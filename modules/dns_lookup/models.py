from dataclasses import dataclass, field

@dataclass(slots=True)
class DNSResult:
    hostname : str
    a_records: list[str] = field(default_factory=list)
    aaaa_records: list[str] = field(default_factory=list)
    mx_records: list[str] = field(default_factory=list)
    ns_records: list[str] = field(default_factory=list)

    cname_records: list[str] = field(default_factory=list)
    ptr_records: list[str] = field(default_factory=list)
