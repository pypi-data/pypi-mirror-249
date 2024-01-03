def find_word_in_file(file_path, target_word):
    indice_line = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("The specified file does not exist.")
        msg = "The specified file does not exist."
        return False, msg

    matching_lines = [index + 1 for index, line in enumerate(lines) if target_word in line]

    if matching_lines:
        print(f"'{target_word}' found in the following lines:")
        for line_number in matching_lines:
            print(f"Line {line_number}: {lines[line_number - 1].strip()}")
            indice_line['line '+str(line_number)] = lines[line_number - 1].strip()
        return True, indice_line
    else:
        print(f"No occurrences of '{target_word}' found in the file.")
        msg = f"No occurrences of '{target_word}' found in the file."
        return False , msg