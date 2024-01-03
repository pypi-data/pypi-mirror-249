def replace_lines_in_range(file_path, action, *args, replacement_string):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("The specified file does not exist.")
        msg = "The specified file does not exist."
        return False, msg
    
    if action == "replace_from_lineX_to_lineY" and len(args) == 2:
        if args[0] > 0 and args[1] <= len(lines):
            # Replace the content of the first line
            lines[args[0] - 1] = replacement_string+'\n'

            for i in range(args[0], args[1]):
                lines[i] = ""

            with open(file_path, 'w') as file:
                file.writelines(lines)
        else:
            print("Invalid line range specified.")
            msg = "Invalid line range specified."
            return False, msg
    elif action == "replace_the_lineX" and len(args) == 1:
        if 1 <= args[0] <= len(lines):
            # Replace the content of the specified line
            lines[args[0] - 1] = "".join(replacement_string)+"\n"

            with open(file_path, 'w') as file:
                file.writelines(lines)
        else:
            print("Invalid target line specified.")
            msg = "Invalid line range specified."
            return False, msg
        
    elif action == "replace_line_start_with" and len(args) == 1 and isinstance(args[0], str):
        for i in range(len(lines)):
            if lines[i].strip().startswith(args[0]):
                # Replace the content of lines starting with the specified word
                lines[i] = replacement_string + "\n"
        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print("Invalid action or arguments.")
        msg = "Invalid action or arguments."
        return False, msg
    
replacement_string = "test dzada "

replace_lines_in_range("/etc/squid/squid1.conf", "replace_from_lineX_to_lineY", 1,3, replacement_string=replacement_string)

replace_lines_in_range("/etc/squid/squid1.conf", "replace_the_lineX", 1, replacement_string=replacement_string)

replace_lines_in_range("/etc/squid/squid1.conf", "replace_line_start_with", "http_access deny violence",replacement_string=replacement_string)

