from .models import DNSResult
from dns import resolver,reversename 
from .exceptions import DNSLookupError,DNSResolverError,DomainNotFoundError

class DNSLookup:
    def __init__(self, hostname):
        self.hostname =  hostname

    def resolve_record(self, record_type:str) -> list[str]:
        try:
            answers = resolver.resolve(self.hostname,record_type)
        except resolver.NXDOMAIN:
            raise DomainNotFoundError(self.hostname)
        except resolver.NoAnswer:
            return []
        except resolver.LifetimeTimeout:
            raise DNSResolverError("DNS query timed out!")
        except resolver.NoNameservers:
            raise DNSResolverError("No DNS nameservers available!")
        return [str(answer) for answer in answers]

    def lookup_a(self) -> list[str]: 
        return self.resolve_record("A")
    
    def lookup_aaaa(self)->list[str]: 
        return self.resolve_record("AAAA")

    def lookup_mx(self)->list[str]: 
        return self.resolve_record("MX")

    def lookup_ns(self)->list[str]: 
        return self.resolve_record("NS")

    def lookup_cname(self)->list[str]:
        return self.resolve_record("CNAME")

    def lookup_ptr(self,ip)->list[str]:
        try:
            reverse_name = reversename.from_address(ip)
            answers = (resolver.resolve(reverse_name,"PTR"))
            return [str(answer) for answer in answers]
        except resolver.NoAnswer:
            return []
        except resolver.NXDOMAIN:
            return []
        except resolver.LifetimeTimeout:
            raise DNSResolverError("DNS query timed out!")
        except resolver.NoNameservers:
            raise DNSResolverError("No DNS nameservers available!")

    def lookup(self) -> DNSResult:
        result = DNSResult(hostname=self.hostname)
        result.a_records = self.lookup_a()
        result.aaaa_records = self.lookup_aaaa()
        result.mx_records = self.lookup_mx()
        result.ns_records = self.lookup_ns()
        result.cname_records = self.lookup_cname()

        for ip_address in result.a_records:
            result.ptr_records.extend(self.lookup_ptr(ip_address))
        
        return result
