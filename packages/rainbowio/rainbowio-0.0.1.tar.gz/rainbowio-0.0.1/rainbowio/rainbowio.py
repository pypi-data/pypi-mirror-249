def print_rgb(color: str, text: str):
    """
    Reads the color and text and prints the text with the specified color\n
    Some of the colors are:\n
    *red*
    *green*
    *blue*\n
    *yellow*
    *magenta*
    *cyan*
    *white*
    """
    match color:
        case "red":
            print(f"\033[91m{text}\033[0m")
        case "green":
            print(f"\033[92m{text}\033[0m")
        case "blue":
            print(f"\033[94m{text}\033[0m")
        case "yellow":
            print(f"\033[93m{text}\033[0m")
        case "magenta":
            print(f"\033[95m{text}\033[0m")
        case "cyan":
            print(f"\033[96m{text}\033[0m")
        case "white":
            print(f"\033[97m{text}\033[0m")

def input_rgb(color: str, text: str):
    """
    Reads the color and text and creates the input with the specified color and text\n
    Some of the colors are:\n
    *red*
    *green*
    *blue*\n
    *yellow*
    *magenta*
    *cyan*
    *white*
    """
    match color:
        case "red":
            return input(f"\033[91m{text}\033[0m")
        case "green":
            return input(f"\033[92m{text}\033[0m")
        case "blue":
            return input(f"\033[94m{text}\033[0m")
        case "yellow":
            return input(f"\033[93m{text}\033[0m")
        case "magenta":
            return input(f"\033[95m{text}\033[0m")
        case "cyan":
            return input(f"\033[96m{text}\033[0m")
        case "white":
            return input(f"\033[97m{text}\033[0m")