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

class PortScanner:
    def __init__(self,hostname,timeout=1,max_workers=100):
        self.hostname=hostname
        self.open_ports: list[PortInfo] = []
        self.timeout=timeout
        self.max_workers=max_workers

    def resolve_hostname(self):
        try:
            ip = socket.gethostbyname(self.hostname)
        except socket.gaierror:
            raise exceptions.HostResolutionError(self.hostname)
        else:
            return ip

    def scan_port(self,ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.timeout)
        
            result = skt.connect_ex((ip,port))
            return result == 0

    def scan_ports(self,ip,ports):
        self.open_ports.clear()
        future_to_port = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:  
            for port in ports:
                future = executor.submit(self.scan_port,ip,port)
                future_to_port[future] = port
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            is_open = future.result()
            if is_open:
                self.open_ports.append(PortInfo(port=port,
                                                service=COMMON_PORTS.get(port,"unknown"),
                                                status="OPEN"))
        self.open_ports.sort(key=lambda port: port.port)
        return self.open_ports
    
    def scan_range(self, target_ip):
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
        if start_port > end_port: raise exceptions.ErrorPortOrdering(start_port,end_port)
        ports=range(start_port,end_port+1)
        self.open_ports=self.scan_ports(target_ip,ports)

    def scan(self):
        try:
            target_ip = self.resolve_hostname()
            option = int(input("Search by\n1. Range of ports\n2. Common ports\nchoose: "))
            if option == 1:
                self.scan_range(target_ip)          
            elif option == 2:
                self.open_ports=self.scan_ports(target_ip,COMMON_PORTS.keys())
            else:
                raise exceptions.InvalidOption
        except exceptions.HostResolutionError as e:
            print(e)
            return None
        except exceptions.InvalidOption as e:
            print(e)
            return None
        except exceptions.ErrorPortOrdering as e:
            print(e) 
            return None
        else:
            return self.open_ports