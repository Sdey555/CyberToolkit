from modules.port_scanner.scanner import PortScanner
from modules.dns_lookup.dns_lookup import DNSLookup
from cli.input import port_scanner_input, dns_lookup_input
from cli.output import display_port_scan_result, display_dns_lookup_result
from cli.user_menu import queryTypeMenu
from core.exceptions import Core_Exception, InvalidOption

def core_handler():
    while(True):
        try:
            choice = queryTypeMenu()
            if choice == 1:
                host, start, end, opt = port_scanner_input()
                port_scanner = PortScanner(host)

                result = port_scanner.scan(start_port=start,end_port=end,option=opt)
                if result:
                    display_port_scan_result(result)
                else:
                    print("Scan Aborted due to error!!")
            elif choice == 2:
                host = dns_lookup_input()
                DNS_lookup = DNSLookup(host)
                result = DNS_lookup.lookup()
                display_dns_lookup_result(result)

            elif choice == 0:
                print("Exiting...")
                break
            else:
                raise InvalidOption
        except Core_Exception as e:
            print(e)