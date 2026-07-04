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