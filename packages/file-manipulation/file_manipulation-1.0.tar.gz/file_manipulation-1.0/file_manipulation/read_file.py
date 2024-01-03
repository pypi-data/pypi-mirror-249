def readFile(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return True,lines
    except FileNotFoundError:
        print("The specified file does not exist.")
        msg = "The specified file does not exist."
        return False, msg