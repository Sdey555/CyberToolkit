import socket
import exceptions
from services import COMMON_PORTS
from dataclasses import dataclass

@dataclass
class PortInfo:
    port: int
    service: str
    status: str = "CLOSED"

class PortScanner:
    def __init__(self,hostname):
        self.hostname=hostname
        self.open_ports: list[PortInfo] = []

    def resolve_hostname(self):
        try:
            ip = socket.gethostbyname(self.hostname)
        except socket.gaierror:
            raise exceptions.HostResolutionError(self.hostname)
        else:
            return ip

    def scan_port(self,ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(1)
        
            result = skt.connect_ex((ip,port))
            return result == 0

    def scan_ports(self,ip,ports):
        for port in ports:
            if self.scan_port(ip,port):
                self.open_ports.append(PortInfo(
                    port=port,
                    service=COMMON_PORTS.get(port,"unknown"),
                    status="OPEN"
                ))
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
            option = int(input("Search by (1. Range of ports, 2. Common ports) : "))
            if option == 1:
                self.scan_range(target_ip)          
            elif option == 2:
                self.open_ports=self.scan_ports(target_ip,COMMON_PORTS.keys())
        except exceptions.HostResolutionError as e:
            print(e)
            return False
        except exceptions.ErrorPortOrdering as e:
            print(e) 
            return False
        else:
            return True

    def show_open_ports(self):
        print("\nScan complete!\n")
        print("\t  Port\tService\tStatus")
        print("\t-----------------")
        if not self.open_ports:
            print("No port is open!")
        else:
            for port_info in self.open_ports:
                print(f"\t  {port_info.port}"
                    f"\t{port_info.service}"
                    f"\t{port_info.status}")