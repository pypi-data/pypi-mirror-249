def uncomment_lines(file_path, action, *args):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("The specified file does not exist.")
        msg = "The specified file does not exist."
        return False, msg

    if action == "uncomment_from_lineX_to_lineY" and len(args) == 2:
        if args[0] > 0 and args[1] <= len(lines):
            for i in range(args[0] - 1, args[1]):
                lines[i] = lines[i].lstrip('#')
                
            with open(file_path, 'w') as file:
                file.writelines(lines)
                
            msg = f"From line {args[0]} to the line {args[1]} is uncommented successfully"
            return True, msg
        
        else:
            print("Invalid target line specified.")
            msg = "Invalid line range specified."
            return False, msg
    elif action == "uncomment_the_lineX" and len(args) == 1:
        if args[0] > 0 and args[0] <= len(lines):
            lines[args[0] - 1] = lines[args[0] - 1].lstrip('#')
            
            with open(file_path, 'w') as file:
                file.writelines(lines)
            
            msg = f"the line {args[0]} is uncommented successfully"
            return True, msg    
        
        else:
            print("Invalid target line specified.")
            msg = "Invalid line range specified."
            return False, msg
                
    elif action == "uncomment_line_start_with" and len(args) == 1 and isinstance(args[0], str):
        for i in range(len(lines)):
            if lines[i].strip().startswith('#' + args[0]):
                lines[i] = lines[i].lstrip('#')
            else:
                print(f"you dons't have a line that start with {args[0]}")
                msg = f"you dons't have a line that start with {args[0]}"
                return False, msg
            
        with open(file_path, 'w') as file:
            file.writelines(lines)
            
        msg = f"the line start with {args[0]} is uncommented successfully"
        return True, msg
    
    else:
        print("Invalid action or arguments.")
        msg = "Invalid action or arguments."
        return False, msg


# uncomment_lines("/etc/squid/squid1.conf", "uncomment_from_lineX_to_lineY", 2, 3)
# uncomment_lines("/etc/squid/squid1.conf", "uncomment_the_lineX", 4)
# uncomment_lines("/etc/squid/squid1.conf", "uncomment_line_start_with", "acl Safe_ports port 80")

