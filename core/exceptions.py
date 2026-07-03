class RequestTimeout(Exception):
    pass
class ErrorPortOrdering(Exception):
    def __init__(self,start,end):
        self.start_port=start
        self.end_port=end

        super().__init__(
            f"Start port {self.start_port} can't be greater than End port {self.end_port}"
        )

class HostResolutionError(Exception):
    def __init__(self,hostname):
        self.hostname=hostname

        super().__init__(
            f"Error! Unable to resolve hostname: {hostname}."
        )

class InvalidOption(Exception):
    def __init__(self): super().__init__("Invalid Option")