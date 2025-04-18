from tabulate import tabulate

def create_menu_options(options_to_create):
    options: list[tuple[int, str]] = {}

    for index, option in enumerate(options_to_create):
        options[index+1] = option

    return options

def show_menu(options):
    print("\n")
    print(tabulate(options.items(), headers=["Option No.", "Options"], tablefmt="psql"))
    print("\n")
    return 

def show_options(rows, columns):
    print("\n")
    print(tabulate(rows, headers=columns, tablefmt="psql"))
    print("\n")
    return 

def show_results(rows, columns):
    print("\n")
    print(tabulate(rows, headers=columns, tablefmt="psql"))
    print("\n")
    return 

def validate_text_input(message, accept_none=False):
    choice = input(message + " ")
    if not accept_none and choice == "":
        while True:
            choice = input("A value is required. Please try again: ")
            if choice != "":
                return choice
    return choice

def validate_option_input(start, end, accept_none=False):
    input_str = input("Please select an option number from above: ")

    if accept_none and input_str == "":
        return input_str
    
    while True:
        int_input = 0
        try:
            int_input = int(input_str)
            if int_input >= start and int_input <= end:
                return int_input
        except:
            None

        input_str = input("Input incorrect. Please enter a valid value: ")
 
def validate_y_n_input(question):
    input_str = input(question + "(y/n): ")
    while True:
        if input_str in ["y", "n"]:
            return input_str
        
        input_str = input("Input incorrect. Please enter a valid response (y/n): ")

def validate_multi_fields_input(options):
    input_str = input("Please enter the numbers of the fields of interest, seperated by spaces, e.g. 1 3 6: ")
    while True:
        try:
            if input_str == "":
                raise Exception
            int_list = [ int(x) for x in input_str.split()]
            if len(options.keys()) != len(int_list):
                return int_list
        except:
            input_str = input("Input incorrect. Please enter a valid response: ")

def press_enter():
    input("Press enter to return...")
        
        