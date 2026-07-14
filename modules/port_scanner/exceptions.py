from core.exceptions import Core_Exception
class PortScannerError(Core_Exception):
    pass
class RequestTimeout(PortScannerError):
    pass
class ErrorPortOrdering(PortScannerError):
    def __init__(self,start,end):
        self.start_port=start
        self.end_port=end

        super().__init__(
            f"Start port {self.start_port} can't be greater than End port {self.end_port}"
        )

class HostResolutionError(PortScannerError):
    def __init__(self,hostname):
        self.hostname=hostname

        super().__init__(
            f"Error! Unable to resolve hostname: {hostname}."
        )

class InvalidOption(PortScannerError):
    def __init__(self): super().__init__("Invalid Option")