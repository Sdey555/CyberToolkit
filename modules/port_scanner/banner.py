import socket
import modules.port_scanner.models as models

class BannerGrabber:
    def __init__(self,hostname:str,timeout:float):
        self.hostname = hostname
        self.timeout = timeout

    def grab_banner(self,ip:str,port_info:models.PortInfo) -> str | None:
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