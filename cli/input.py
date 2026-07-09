def user_input():
    host = input("Enter Hostname or IP: ")
    option = int(input("Search by\n1. Range of ports\n2. Common ports\nchoose: "))
    if option == 1:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
        return host,start_port,end_port,option
    elif option == 2:
        return host,None,None,option