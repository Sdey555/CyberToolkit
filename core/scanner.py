import socket
from core import exceptions
from core.services import COMMON_PORTS
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class PortInfo:
    port: int
    service: str
    status: str = "CLOSED"
    banner: str | None = None

class PortScanner:
    def __init__(self,hostname,timeout=1,max_workers=100):
        self.hostname=hostname
        self.open_ports: list[PortInfo] = []
        self.timeout=timeout
        self.max_workers=max_workers

    def resolve_hostname(self):
        try:
            return socket.gethostbyname(self.hostname)
        except socket.gaierror:
            raise exceptions.HostResolutionError(self.hostname)
        
    def grab_banner(self,ip,port_info):
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
            
    def grab_http_banner(self,sock):
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
    
    def scan_port(self,ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.timeout)
        
            result = skt.connect_ex((ip,port))
            if result==0:
                return PortInfo(port=port,
                                service=COMMON_PORTS.get(port,"unknown"),
                                status="OPEN")
            else:
                return None

    def scan_ports(self,ip,ports):
        self.open_ports.clear()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scan_port,ip,port) for port in ports}
        for future in as_completed(futures):
            port_info = future.result()
            if port_info:
                port_info.banner =  self.grab_banner(ip,port_info) 
                self.open_ports.append(port_info)
        self.open_ports.sort(key=lambda port_info: port_info.port)
        return self.open_ports
    
    def scan_range(self,target_ip,start_port,end_port):
        if start_port > end_port: raise exceptions.ErrorPortOrdering(start_port,end_port)
        ports=range(start_port,end_port+1)
        return self.scan_ports(target_ip,ports)

    def scan(self,start_port,end_port,option):
        try:
            target_ip = self.resolve_hostname()
            if option == 1:
                return self.scan_range(target_ip,start_port,end_port)          
            elif option == 2:
                return self.scan_ports(target_ip,COMMON_PORTS.keys())
            else:
                raise exceptions.InvalidOption
        except (exceptions.HostResolutionError,
                exceptions.InvalidOption,
                exceptions.ErrorPortOrdering) as e:
            print(e)