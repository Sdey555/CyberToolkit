def display_port_scan_result(scan_result):
    
    print("="*40)
    print(" "*7,"Port Scan Summary")
    print("="*40)

    # print("\n----------------------------")
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
            
def display_dns_lookup_result(dns_lookup_result):
    def display_section(record_type, records):
        print(f"\n{record_type}")
        print("-----------------")
        if records:
            for record in records: print(record)
        else: print("None")

    print("="*40)
    print(" "*7,"DNS Lookup Summary")
    print("="*40)

    print(f"\nHostname : {dns_lookup_result.hostname}")
    
    display_section("A Records",dns_lookup_result.a_records)
    display_section("AAAA Records",dns_lookup_result.aaaa_records)
    display_section("MX Records",dns_lookup_result.mx_records)
    display_section("NS Records",dns_lookup_result.ns_records)
    display_section("CNAME Records",dns_lookup_result.cname_records)
    display_section("PTR Records",dns_lookup_result.ptr_records)