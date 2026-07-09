from core.scanner import PortScanner
from cli.input import user_input
from cli.output import display_scan_result

host,start,end,opt = user_input()
port_scanner = PortScanner(host)

result = port_scanner.scan(start,end,opt)
if result:
    display_scan_result(result)
else:
    print("Scan Aborted due to error!")