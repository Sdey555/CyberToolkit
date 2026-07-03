from core.scanner import PortScanner

port_scanner = PortScanner(input("Enter Hostname or IP: "))

def display_scan_result(port_list):
    print("\nScan complete!\n")
    
    if not port_list:
        print("No port is open!")
    else:
        print(f"{'Port':<8}{'Service':<12}{'Status'}")
        print("-------------------------------------")
        for port_info in port_list:
            print(f"{port_info.port:<8}"
                f"{port_info.service:<12}"
                f"{port_info.status}")

result = port_scanner.scan()
if result:
    display_scan_result(result)
else:
    print("Scan Aborted due to error!")