import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import random
import string
from argon2 import PasswordHasher
import colorama
from colorama import Back, Style

colorama.init()

if os.name == 'nt':
    try:
        import msvcrt
    except ImportError:
        print("Failed to import msvcrt on Windows.")
        exit(1)
else:
    try:
        import termios
        import tty
    except ImportError:
        print("Failed to import termios/tty on Linux.")
        exit(1)

def hash(text):
    """
    Hashes the input text using Argon2.

    Parameters:
    - text (str): The text to be hashed.

    Returns:
    - str: The hashed text.
    """
    ph = PasswordHasher()
    hashed_password = ph.hash(text)
    return hashed_password

def verify_hash(hashed_text, text):
    """
    Verifies the text against the provided hashed text.

    Parameters:
    - hashed_text (str): The hashed text.
    - text (str): The text to be verified.

    Returns:
    - bool: True if the verification is successful, False otherwise.
    """
    ph = PasswordHasher()
    try:
        is_valid = ph.verify(hashed_text, text)
        return is_valid
    except:
        return False

def code(code_length):
    """
    Generates a random code of the specified length.

    Parameters:
    - code_length (int): The length of the generated code.

    Returns:
    - str: The randomly generated code.
    """
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(code_length))
    return code

def detect_input():
    """
    Detects user input (up, down, enter) depending on the operating system.

    Returns:
    - str: The detected user input.
    """
    if os.name == 'nt':  # Windows
        try:
            import msvcrt
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    return 'up'
                elif key == b'P':
                    return 'down'
            elif key == b'\r':
                return 'enter'
            return key.decode('utf-8')
        except ImportError:
            print("Failed to import msvcrt on Windows.")
            exit(1)
    else:  # Linux
        try:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                if key == '\x1b':
                    key = sys.stdin.read(2)
                    if key == '[A':
                        return 'up'
                    elif key == '[B':
                        return 'down'
                elif key == '\r':
                    return 'enter'
                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except ImportError:
            print("Failed to import termios/tty on Linux.")
            exit(1)

def foreground(text, color):
    """
    Changes the color of the text (the Foreground) when printed.

    Parameters:
    - text (str): The text to be colored.
    - color (str): The desired color. Supported colors: 'white', 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'light_gray', 'dark_gray', 'light_red', 'light_green', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan', 'reset'.

    Returns:
    - str: The colored text.
    """
    color_code = {
        'white': '97',
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'light_gray': '37',
        'dark_gray': '90',
        'light_red': '91',
        'light_green': '92',
        'light_yellow': '93',
        'light_blue': '94',
        'light_magenta': '95',
        'light_cyan': '96',
        'reset': '0',
    }

    if color.lower() in color_code:
        return f"\033[{color_code[color.lower()]}m{text}\033[0m"
    else:
        return text  # Return the text as is if the color is not found in the dictionary

def highlight(text, color):
    """
    Sets the highlight color of the text when printed.

    Parameters:
    - text (str): The text to be highlighted.
    - color (str): The color for highlighting. Supported colors: 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'reset'.

    Returns:
    - str: The highlighted text.
    """
    color_codes = {
        'red': Back.RED,
        'green': Back.GREEN,
        'yellow': Back.YELLOW,
        'blue': Back.BLUE,
        'magenta': Back.MAGENTA,
        'cyan': Back.CYAN,
        'white': Back.WHITE,
        'reset': Style.RESET_ALL  # Reset color to default
    }

    # Check if the specified color is supported
    if color not in color_codes:
        raise ValueError(f"Unsupported color: {color}. Choose from {', '.join(color_codes.keys())}")
    else:
        return color_codes[color] + text + color_codes['reset']

def clear_last_x_lines(lines_to_clear):
    """
    Clears the specified number of lines in the console.

    Parameters:
    - lines_to_clear (int): The number of lines to clear.
    """
    if os.name == 'posix':
        for _ in range(lines_to_clear):
            print("\033[F\033[K", end="")  # Move up and clear line
    elif os.name == 'nt':
        for temp in range(lines_to_clear):
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
    else:
        for _ in range(lines_to_clear):
            print('\033[A\033[K', end='')

def radio_choice(choice, selection_foreground='black', selection_highlight='white'):
    """
    Displays a radio-style choice menu and allows the user to select an option.

    Parameters:
    - choice (list): The list of choices.
    - selection_foreground (str): The foreground color for the selected option.
    - selection_highlight (str): The highlight color for the selected option.

    Returns:
    - str: The selected option.
    """
    i = 0
    a = 0
    while True:
        for x in choice:
            if i == a:
                try:
                    print(foreground(highlight(x, selection_highlight), selection_foreground))
                except:
                    selection_foreground = 'black'
                    selection_highlight = 'white'
                    print(foreground(highlight(x, selection_highlight), selection_foreground))
            else:
                print(x)
            a += 1
            if a == len(choice):  # Reset 'a' to 0 when it reaches the end of the list
                a = 0
        user_input = detect_input()
        if user_input == 'up' and i > 0:
            i -= 1
        elif user_input == 'down' and i < len(choice) - 1:
            i += 1
        elif user_input == 'enter':
            return choice[i]
        clear_last_x_lines(len(choice))

def password(min_length=3, max_length=20, warning_message=True):
    """
    Takes user input for a password with minimum and maximum length constraints.

    Parameters:
    - min_length (int): The minimum length of the password.
    - max_length (int): The maximum length of the password.
    - warning_message (bool): Whether to display a warning message for invalid password lengths.

    Returns:
    - str: The user-inputted password.
    """
    password = ""
    while True:
        if len(password) > max_length:
            display_password = '*' * (max_length)
        else:
            display_password = '*' * len(password)

        print("Password : ", display_password)
        a = detect_input()

        if a == 'enter':
            if len(password) >= min_length and len(password) <= max_length:
                return password
            elif warning_message:
                clear_last_x_lines(1)
                temp = f"Password must be between {min_length} and {max_length} characters."
                print(highlight(temp, 'white'))
                time.sleep(3)
                clear_last_x_lines(0)
                password = ""
            else:
                password = ""
        elif (a != 'up') and (a != 'down'):
            password = password + a
        clear_last_x_lines(1)

def matrixify(columns, rows, filler):
    """
    Creates a matrix with the specified number of columns, rows, and a filler value.

    Parameters:
    - columns (int): The number of columns in the matrix.
    - rows (int): The number of rows in the matrix.
    - filler (any): The value to fill the matrix with.

    Returns:
    - list: The created matrix.
    """
    xyz = [[filler] * columns for _ in range(rows)]
    return xyz

def contains(matrix, string):
    """
    Checks if a matrix contains a specific string.

    Parameters:
    - matrix (list): The matrix to search.
    - string (any): The string to check for in the matrix.

    Returns:
    - bool: True if the string is found, False otherwise.
    """
    for row in matrix:
        if string in row:
            return True
    return False

def replace(matrix, string, filler):
    """
    Replaces all occurrences of a specific string in a matrix with a new value.

    Parameters:
    - matrix (list): The matrix to modify.
    - string (any): The string to replace.
    - filler (any): The value to replace the string with.

    Returns:
    - list: The modified matrix.
    """
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] == string:
                matrix[x][y] = filler
    return matrix

def webscrape(url):
    """
    Scrapes a web page and returns the BeautifulSoup object or an error code.

    Parameters:
    - url (str): The URL of the web page to scrape.

    Returns:
    - BeautifulSoup or int: The BeautifulSoup object representing the parsed HTML or an error code.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            return response.status_code
    except:
        return "Error while scraping:" + url

def clean_text(text):
    """
    Cleans and standardizes text by removing punctuation and ensuring it ends with a period.

    Parameters:
    - text (str): The text to be cleaned.

    Returns:
    - str: The cleaned and standardized text.
    """
    # Remove all punctuation except full stops
    translator = str.maketrans('', '', string.punctuation.replace('.', ''))
    cleaned_text = text.translate(translator)

    # Replace exclamation marks and question marks with full stops
    cleaned_text = cleaned_text.replace('!', '.').replace('?', '.')

    # Ensure the text ends with a full stop and convert to lowercase
    cleaned_text = cleaned_text.strip()
    if not cleaned_text.endswith('.'):
        cleaned_text += '.'
    cleaned_text = cleaned_text.lower()

    return cleaned_text.upper()

def morse(text):
    """
    Converts cleaned text to Morse code format.

    Parameters:
    - text (str): The text to be converted to Morse code.

    Returns:
    - str: The Morse code representation of the input text.
    """
    text = clean_text(text)
    words = text.split()
    Morse = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": "._.",
        "S": "...",
        "T": "-",
        "U": "..--",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
    }
    temp = []
    output = []
    for x in words:
        temp.append(list(x))
    letters = [char for sublist in temp for char in sublist]
    for i in letters:
        morse_code = Morse.get(i, 'None')
        if morse_code != 'None':
            output.append(morse_code)
    return ' '.join(output)

def display(matrix):
    """
    Displays the contents of a matrix in a readable format.

    Parameters:
    - matrix (list): The matrix to be displayed.
    """
    for row in matrix:
        print(row)

def replace_index(matrix, x, y, filler):
    """
    Replaces the value at a specified index in a matrix with a new value.

    Parameters:
    - matrix (list): The matrix to be modified.
    - x (int): The row index.
    - y (int): The column index.
    - filler (any): The value to replace the existing value.
    """
    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
        matrix[x][y] = filler
    else:
        print("Index out of range.")
        
def help():
	functions = [
        ("hash(text)", "Hashes the input text using Argon2."),
        ("verify_hash(hashed_text, text)", "Verifies the text against the provided hashed text."),
        ("code(code_length)", "Generates a random code of the specified length."),
        ("detect_input()", "Detects user input (up, down, enter) depending on the operating system."),
        ("highlight(text, color)", "Sets the highlight color of the text when printed."),
        ("clear_last_x_lines(lines_to_clear)", "Clears the specified number of lines in the console."),
        ("radio_choice(choice)", "Displays a radio-style choice menu and allows the user to select an option."),
        ("password(min_length=3, max_length=20, warning_message=True)", "Takes user input for a password with minimum and maximum length constraints"),
        ("matrixify(columns, rows, filler)", "Creates a matrix with the specified number of columns, rows, and a filler value."),
        ("*display(matrix)", "Displays the contents of a matrix in a readable format."),
        ("*replace_index(matrix, x, y, filler)", "Replaces the value at a specified index in a matrix with a new value."),
        ("contains(matrix, string)", "Checks if a matrix contains a specific string."),
        ("replace(matrix, string, filler)", "Replaces all occurrences of a specific string in a matrix with a new value."),
        ("webscrape(url)", "Scrapes a web page and returns the BeautifulSoup object or an error code."),
        ("clean_text(text)", "Cleans and standardizes text by removing punctuation and ensuring it ends with a period."),
        ("morse(text)", "Converts cleaned text to Morse code format."),
        ("foreground(text, color)", "Changes the color of the text(the Foreground) when printed.")
    ]
	x=1
	for function, description in functions:
		temp = f"{function} - {description}"
		if x%2 == 0:
			print(foreground(temp,'white'))
		else:
			print(foreground(temp,'red'))
		x=x+1
        
