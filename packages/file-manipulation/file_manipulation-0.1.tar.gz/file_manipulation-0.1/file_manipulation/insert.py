def insert_lines(file_path, action, *args,insert_string):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("The specified file does not exist.")
        msg = "The specified file does not exist."
        return False, msg
    
    if action == "insert_before" and len(args) == 1 and isinstance(args[0], int):
        lines.insert(args[0] - 1, f"{insert_string}\n")
        
    elif action == "insert_after" and len(args) == 1 and isinstance(args[0], int):
        lines.insert(args[0], f"{insert_string}\n")
        print(f"Line inserted after {args[0]}: {insert_string}")
        msg = f"Line inserted after {args[0]}: {insert_string}"
        
    # elif action == "insert_between" and len(args) == 2 and all(isinstance(arg, int) for arg in args):
    #     start, end = args
    #     lines.insert(end - 1, f"{insert_string}\n")
    #     print(f"Line inserted between {start} and {end}: {insert_string}")
    #     msg = f"Line inserted between {start} and {end}: {insert_string}"
        
    else:
        print("Invalid action or arguments.")
        msg = "Invalid action or arguments."
        return False, msg
    
    with open(file_path, 'w') as file:
        file.writelines(lines)
        
insert_string = "zafafzafa"       
# insert_lines("/etc/squid/squid1.conf",'insert_after',6,insert_string=insert_string)
insert_lines("/etc/squid/squid1.conf",'insert_before',2,insert_string=insert_string)