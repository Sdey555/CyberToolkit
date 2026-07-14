import socket
from modules.port_scanner import exceptions
from modules.port_scanner.services import COMMON_PORTS
import modules.port_scanner.models as models
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from collections.abc import Iterable
from modules.port_scanner.banner import BannerGrabber

class PortScanner:
    def __init__(self,hostname:str,timeout:float=1,max_workers:int=100):
        self.hostname=hostname
        self.open_ports: list[models.PortInfo] = []
        self.timeout=timeout
        self.max_workers=max_workers
        self.scan_stats = models.ScanStats(self.hostname,None,0,0,0.0)

    def resolve_hostname(self) -> str:
        try:
            return socket.gethostbyname(self.hostname)
        except socket.gaierror:
            raise exceptions.HostResolutionError(self.hostname)
        
    def reset(self):
        self.scan_stats.target = self.hostname
        self.scan_stats.open_port_count=0
        self.scan_stats.port_count=0
        self.scan_stats.total_time=0.0
        self.open_ports.clear()
    
    def scan_port(self,ip:str, port:int) -> models.PortInfo | None:
        start_time = time.perf_counter()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.timeout)
        
            result = skt.connect_ex((ip,port))
            end_time = time.perf_counter()
            if result==0:
                return models.PortInfo(port=port,
                                service=COMMON_PORTS.get(port,"unknown"),
                                status="OPEN",
                                latency=(end_time-start_time))
            else:
                return None

    def scan_ports(self,ip:str,ports:Iterable[int]) -> list[models.PortInfo]:
        self.scan_stats.port_count=len(ports)
        start_time = time.perf_counter()
        self.reset()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scan_port,ip,port) for port in ports}
        for future in as_completed(futures):
            port_info = future.result()
            if port_info:
                self.scan_stats.open_port_count+=1
                grabber = BannerGrabber(self.hostname,self.timeout)
                port_info.banner = grabber.grab_banner(ip,port_info)
                self.open_ports.append(port_info)
        end_time = time.perf_counter()
        self.scan_stats.total_time = (end_time-start_time)
        self.open_ports.sort(key=lambda port_info: port_info.port)
        return self.open_ports
    
    def scan_range(self,target_ip:str,start_port:int,end_port:int) -> list[models.PortInfo]:
        if start_port > end_port: raise exceptions.ErrorPortOrdering(start_port,end_port)
        ports=range(start_port,end_port+1)
        return self.scan_ports(target_ip,ports)

    def scan(self,start_port,end_port,option) -> models.ScanResult | None:
        self.scan_stats.resolved_ip = target_ip = self.resolve_hostname()
        if option == 1:
            return models.ScanResult(ports_info=self.scan_range(target_ip,start_port,end_port),
                                        stats=self.scan_stats)        
        elif option == 2:
            return models.ScanResult(ports_info=self.scan_ports(target_ip,COMMON_PORTS.keys()),
                                        stats=self.scan_stats)
        else:
            raise exceptions.InvalidOption