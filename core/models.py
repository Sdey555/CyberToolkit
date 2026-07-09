from dataclasses import dataclass

@dataclass
class PortInfo:
    port: int
    service: str
    status: str = "CLOSED"
    banner: str | None = None
    latency: float | None = None

@dataclass(slots=True)
class ScanStats:
    target: str 
    resolved_ip: str
    port_count: int
    open_port_count: int
    total_time: float

@dataclass(slots=True)
class ScanResult:
    ports_info: list[PortInfo]
    stats: ScanStats