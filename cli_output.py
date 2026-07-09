def display_scan_result(scan_result):
    print("\nScan complete!\n")

    print("Scan Summary")
    print("\n----------------------------")
    print(f"\nTarget: {scan_result.stats.target}\nResolved IP: {scan_result.stats.resolved_ip}")
    print("\n-----------------------------------------------------")
    print(f"\nPorts scanned: {scan_result.stats.port_count}"
          f"\nOpen Ports: {scan_result.stats.open_port_count}"
          f"\nTime elapsed: {scan_result.stats.total_time:.2f} s\n")

    if not scan_result.ports_info:
        print("No port is open!")
    else:
        print(f"{'Port':<8}{'Service':<12}{'Status':<16}{'Latency':<18}{'Banner'}")
        print("---------------------------------------------------------------------")
        for port_info in scan_result.ports_info:
            print(f"{port_info.port:<8}"
                f"{port_info.service:<12}"
                f"{port_info.status:<16}"
                f"{port_info.latency*1000:.2f} ms{'':<12}"
                f"{port_info.banner}")