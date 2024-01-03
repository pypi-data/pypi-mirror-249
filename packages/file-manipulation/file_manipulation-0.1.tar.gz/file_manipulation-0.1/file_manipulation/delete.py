def delete_lines(file_path, action, *args):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("The specified file does not exist.")
        msg = "The specified file does not exist."
        return False, msg
    
    if action == "delete_from_lineX_to_lineY" and len(args) == 2:
        if args[0] > 0 and args[1] <= len(lines):
            del lines[args[0] - 1:args[1]]
            with open(file_path, 'w') as file:
                file.writelines(lines)
                
    elif action == "delete_the_lineX" and len(args) == 1:
        if args[0] > 0 and args[0] <= len(lines):
            del lines[args[0] - 1]
            with open(file_path, 'w') as file:
                file.writelines(lines)
                
    elif action == "delete_line_start_with" and len(args) == 1 and isinstance(args[0], str):
        lines = [line for line in lines if not line.strip().startswith(args[0])]
        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print("Invalid action or arguments.")
        msg = "Invalid action or arguments."
        return False, msg

delete_lines("/etc/squid/squid1.conf", "delete_from_lineX_to_lineY", 2, 7)
delete_lines("/etc/squid/squid1.conf", "delete_the_lineX", 1)
delete_lines("/etc/squid/squid1.conf", "delete_line_start_with", "acl SSL_ports port 443")
