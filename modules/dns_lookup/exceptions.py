from core.exceptions import Core_Exception
class DNSLookupError(Core_Exception):
    def __init__(self,*args):
        super().__init__(*args)

class DomainNotFoundError(DNSLookupError):
    def __init__(self,hostname):
        super().__init__(
            f"Error!! {hostname} Domain not found!!"
        )

class DNSResolverError(DNSLookupError):
    def __init__(self,msg):
        super().__init__(
            f"{msg}"
        )
