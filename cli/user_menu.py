from core.exceptions import InvalidOption
def queryTypeMenu():
    options = {1:'Port Scanner',
               2:'DNS Lookup'}

    print("="*40)
    print(" "*10,"CyberToolkit v1.3")
    print(" "*5,"A Python Cybersecurity Tool")
    print("="*40)
    print("\n")
    for option in options:
        print(f"{option}. {options.get(option)}\n")
    print("0. Exit\n")
    try:
        choice = int(input("Choice: "))
    except ValueError:
        raise InvalidOption
    print("\n")
    return choice
