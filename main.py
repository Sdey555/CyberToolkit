from scanner import PortScanner

port_scanner = PortScanner(input("Enter Hostname or IP: "))

if port_scanner.scan():
    port_scanner.show_open_ports()
else:
    print("Scan Aborted due to error!")