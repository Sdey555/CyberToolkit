import socket
from core import exceptions
from core.services import COMMON_PORTS
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from collections.abc import Iterable

@dataclass
class PortInfo:
    port: int
    service: str
    status: str = "CLOSED"
    banner: str | None = None
    latency: float | None = None

@dataclass(slots=True)
class ScanStats:
    target: str 
    resolved_ip: str
    port_count: int
    open_port_count: int
    total_time: float

@dataclass(slots=True)
class ScanResult:
    ports_info: list[PortInfo]
    stats: ScanStats 

class PortScanner:
    def __init__(self,hostname:str,timeout:float=1,max_workers:int=100):
        self.hostname=hostname
        self.open_ports: list[PortInfo] = []
        self.timeout=timeout
        self.max_workers=max_workers
        self.scan_stats = ScanStats(self.hostname,None,0,0,0.0)

    def resolve_hostname(self) -> str:
        try:
            return socket.gethostbyname(self.hostname)
        except socket.gaierror:
            raise exceptions.HostResolutionError(self.hostname)
        
    def grab_banner(self,ip:str,port_info:PortInfo) -> str | None:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            try:
                sock.connect((ip,port_info.port))
                if port_info.service=="http":
                    return self.grab_http_banner(sock)
                else:
                    banner = sock.recv(1024)
                    return banner.decode(errors="ignore").strip()
            except (socket.timeout,
               ConnectionResetError,
               OSError):
                return None
            
    def grab_http_banner(self,sock:socket.socket) -> str | None:
        request = f"GET / HTTP/1.1\r\nHost: {self.hostname}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode("utf-8"))
        data = sock.recv(1024)
        data_text = data.decode(errors="ignore")
        lines = data_text.split("\r\n")
        for line in lines:
            if line.lower().startswith("server:"):
                banner = line.split(":",1)[1].strip()
                return banner
        return None
    
    def scan_port(self,ip:str, port:int) -> PortInfo | None:
        start_time = time.perf_counter()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.timeout)
        
            result = skt.connect_ex((ip,port))
            end_time = time.perf_counter()
            if result==0:
                return PortInfo(port=port,
                                service=COMMON_PORTS.get(port,"unknown"),
                                status="OPEN",
                                latency=(end_time-start_time))
            else:
                return None

    def scan_ports(self,ip:str,ports:Iterable[int]) -> list[PortInfo]:
        self.scan_stats.port_count=len(ports)
        start_time = time.perf_counter()
        self.open_ports.clear()
        self.scan_stats.target = self.hostname
        self.scan_stats.open_port_count=0
        self.scan_stats.port_count=0
        self.scan_stats.total_time=0.0
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scan_port,ip,port) for port in ports}
        for future in as_completed(futures):
            port_info = future.result()
            if port_info:
                self.scan_stats.open_port_count+=1
                port_info.banner =  self.grab_banner(ip,port_info) 
                self.open_ports.append(port_info)
        end_time = time.perf_counter()
        self.scan_stats.total_time = (end_time-start_time)
        self.open_ports.sort(key=lambda port_info: port_info.port)
        return self.open_ports
    
    def scan_range(self,target_ip:str,start_port:int,end_port:int) -> list[PortInfo]:
        if start_port > end_port: raise exceptions.ErrorPortOrdering(start_port,end_port)
        ports=range(start_port,end_port+1)
        return self.scan_ports(target_ip,ports)

    def scan(self,start_port,end_port,option) -> ScanResult | None:
        try:
            self.scan_stats.resolved_ip = target_ip = self.resolve_hostname()
            if option == 1:
                return ScanResult(ports_info=self.scan_range(target_ip,start_port,end_port),stats=self.scan_stats)        
            elif option == 2:
                return ScanResult(ports_info=self.scan_ports(target_ip,COMMON_PORTS.keys()),stats=self.scan_stats)
            else:
                raise exceptions.InvalidOption
        except (exceptions.HostResolutionError,
                exceptions.InvalidOption,
                exceptions.ErrorPortOrdering) as e:
            print(e)
