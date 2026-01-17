"""
1.17.26 JHU Agentic AI Password Manager Project 

Create a Python script that performs the following tasks:

1. **Import Libraries:**
   - Import the required libraries:
     - `os`: For interacting with the operating system (not used explicitly in the provided code, but part of the setup).
     - `json`: For handling JSON file operations, such as reading and writing.
     - `datetime`: Although it's imported, it's not used in the provided code, but it might be useful in other parts of the script for logging or time-related operations.

2. **Define File Locations and Names:**
   - Set file paths for three files:
     - `MASTER_LOGIN`: This file will store master login information, with the path set to `master_login.json`.
     - `PASSWORD_FILE`: This file will store application passwords, with the path set to `app_password.json`.
     - `LOG_FILE`: A log file for storing logs, with the path set to `log.txt` (although it's not used in the current logic).

3. **Create Dummy Data:**
   - Define two dictionaries with dummy data:
     - `master_login`: A dictionary that holds usernames as keys and their corresponding passwords as values. The provided example has the following data:
       ```python
       {"Jimmy": "robert@123", "Angela": "2009_Bonnet"}
       ```
     - `app_password`: A dictionary that maps usernames to a list of dictionaries. Each dictionary in the list contains `domain` and `pwd` (password for that domain). The provided example contains:
       ```python
       "Jimmy": [
           {"domain": "Facebook", "pwd": "JimmyGordan"},
           {"domain": "Instagram", "pwd": "B0atm@n"}
       ],
       "Angela": [
           {"domain": "Facebook", "pwd": "NelsonM009"},
           {"domain": "Instagram", "pwd": "Mikcy&Angela"}
       ]
       ```

4. **Write Data to Files:**
   - Use the `json.dump()` method to write the `master_login` and `app_password` data into their respective files:
     - Check if the files are not existing then only create the files.
     - Write the `master_login` data into the `MASTER_LOGIN` file (`master_login.json`).
     - Write the `app_password` data into the `PASSWORD_FILE` file (`app_password.json`).
     - Both JSON files should be formatted with an indentation of 4 spaces for readability.
"""

# Importing Libraries
import os, json
from datetime import datetime

# Initializing file locations and names
MASTER_LOGIN    =   'master_login.json'
PASSWORD_FILE   =   'app_password.json'
LOG_FILE        =   'log.txt'

# Dummy Data
# {"Username":"Password"}
master_login = {"Jimmy":"robert@123",
                "Angela":"2009_Bonnet"}



#  { "Username":[ {"domain":"", "pwd":"" },
#                 {"domain":"", "pwd":"" },... ] }
app_password = {
    "Jimmy": [
        {"domain": "Facebook", "pwd": "JimmyGordan"},
        {"domain": "Instagram", "pwd": "B0atm@n"}
    ],
    "Angela": [
        {"domain": "Facebook", "pwd": "NelsonM009"},
        {"domain": "Instagram", "pwd": "Mikcy&Angela"},
    ]
}

# writing the dummy data into the files
if not os.path.exists(MASTER_LOGIN): #“If the file does NOT already exist…”
    with open(MASTER_LOGIN, 'w+') as file:
        json.dump(master_login, file, indent=4) #convert dictionary to JSON and write to file / serialize the Python dictionary into JSON and write it to the file
    print(f"{MASTER_LOGIN} created and data written.")

if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, 'w+') as file:
        json.dump(app_password, file, indent=4)
    print(f"{PASSWORD_FILE} created and data written.")


# Function to divide a number into four nearly equal parts
def getting_equal_length(num):
    # Divide the number by 4 using integer division
    quotient = num // 4
    remainder = num % 4

    # Create a list with the quotient repeated 4 times
    result = [quotient] * 4

    # Distribute the remainder among the first few elements
    for i in range(remainder):
        result[i] = result[i] + 1

    return result
"""
This function generates a cryptographically secure password while enforcing
character-type requirements.

Instead of selecting all characters from a single pool (which can accidentally
exclude required character types), the password length is first divided into
four nearly equal parts using the helper function `getting_equal_length()`.

Each part corresponds to a required category:
- lowercase letters
- uppercase letters
- digits
- special characters

Random characters are generated securely within each category using
`secrets.choice()`. Once all characters are collected, they are securely
shuffled using `secrets.SystemRandom().shuffle()` to eliminate any predictable
ordering or structure.

This approach ensures:
- The total password length is always correct (even for odd lengths)
- All character categories are represented
- The final password is fully randomized and cryptographically strong
"""
import secrets
import string

def generate_secure_password(length=12):
    distribution = getting_equal_length(length)

    password = []

    password += [secrets.choice(string.ascii_lowercase) for _ in range(distribution[0])]
    password += [secrets.choice(string.ascii_uppercase) for _ in range(distribution[1])]
    password += [secrets.choice(string.digits) for _ in range(distribution[2])]
    password += [secrets.choice(string.punctuation) for _ in range(distribution[3])]    

    #shuffling the password list to avoid any patterns
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

"""
Generates a cryptographically secure password while enforcing character-type requirements.

The total password length (default = 12) is first divided into four nearly equal
parts using `getting_equal_length(length)`. Each part corresponds to a required
character category:
- lowercase letters
- uppercase letters
- digits
- special characters

For each category, the function generates the required number of random characters
using `secrets.choice()`, which provides cryptographically secure randomness suitable
for passwords.

All generated characters are stored in a list, then securely shuffled using
`secrets.SystemRandom().shuffle()` to eliminate any predictable ordering or structure.
Finally, the list of characters is joined into a single string and returned.

This approach ensures:
- The password is always the correct length
- All character categories are represented
- The final output is fully randomized and secure
"""

# Function to read the stored passwords from the file
def read_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to write the passwords to the file
def write_passwords(data):
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to log updates to the password log
def log_update(message):
    with open(LOG_FILE, 'a+') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
"""
Helper functions for managing persistent password storage and logging.

- `read_passwords()` is responsible for safely loading stored password data
  from disk. If the password file does not yet exist (e.g., first run),
  it returns an empty dictionary to prevent errors.

- `write_passwords(data)` persists the in-memory password data by serializing
  the provided dictionary into JSON format and writing it to disk. This
  function overwrites the existing file to ensure the stored data always
  reflects the current application state.

- `log_update(message)` records password-related actions to a log file,
  appending each entry with a timestamp. Logging is intentionally separated
  from core logic so actions can be tracked without affecting program flow.

Together, these functions separate file I/O and logging concerns from the
password manager’s core business logic, making the code safer, clearer,
and easier to maintain.
"""
def add_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Prompt user to enter domain and password
    print("="*40)
    print(f"{'Add Password'.center(40)}")
    print("="*40)

    domain = input("Enter the domain name: ")
    print(f"<======  If you wish to generate a random password, leave the password field as blank. ======>")
    password = input("Enter the password for the domain: ")

    # Generating a random password if the user has not provided the password
    if password == "":
        password = generate_secure_password()

    # Check if the user exists in app_password; if not, initialize an empty list for them
    if uid not in app_password:
        app_password[uid] = []

    # Create a new password entry
    new_entry = { "domain": domain, "pwd": password }

    # Append the new entry to the user's password list
    app_password[uid].append(new_entry)

    # Write the updated password list back to the file
    write_passwords(app_password)

    # Log the action for tracking purposes
    log_update(f"Added password for {domain} under user {uid}")

    # Print success message with a decorative format
    print("*"*40)
    print(f"Password for {domain} has been added successfully.")
    print("*"*40)

"""
Adds a password entry for a given user.

This function loads the existing password data from disk, prompts the user
for a domain and password, and automatically generates a secure password
if none is provided. If the user does not yet have any stored passwords,
an entry is initialized for them.

The new domain/password pair is appended to the user’s password list,
persisted back to storage, and recorded in the log for audit and tracking
purposes. A success message is displayed upon completion.
"""

def retrieve_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Check if the user exists and has stored passwords
    if uid in app_password and app_password[uid]:
        print("="*40)
        print(f"{'Stored Passwords'.center(40)}")  # Title centered
        print("="*40)

        # Enumerate through the list of stored passwords and display the domains
        for index, entry in enumerate(app_password[uid], 1):
            print(f"{index}. {entry['domain']}")  # List the domain name (website)

        # Allow the user to select an option to view a specific password
        try:
            choice = int(input("\nEnter the option number to display the password: "))

            # Validate the user's choice
            if 0 < choice <= len(app_password[uid]):
                selected_entry = app_password[uid][choice - 1]

                # Display the selected password details with decorative formatting
                print("*"*40)
                print(f"Password for {selected_entry['domain']} ==> {selected_entry['pwd']}")
                print("*"*40)
                # Log the password retrival
                log_update(f"Retrieved password for {selected_entry['domain']} under user {uid}")

            else:
                # Invalid option if the choice is out of range
                print("\n[!] Invalid option selected. Please choose a valid number.\n")

        except ValueError:
            # Error message if the user does not input a valid integer
            print("\n[!] Please enter a valid number.\n")

    else:
        # If no passwords are stored or user is not found
        print("\n[!] No passwords stored or user not found.\n")
"""
Retrieves and displays stored passwords for a given user.

The `uid` parameter is expected to be provided by the calling code (e.g., after
a login or user selection step). This function does not prompt for the user ID;
it operates only on the user passed into it.

The function loads all stored password data from disk, verifies that the user
exists and has stored passwords, and then displays a numbered list of domains
associated with that user. The numbering is generated using `enumerate()`,
which provides both a human-friendly index (starting at 1) and the actual
password entry during iteration.

The user is prompted to select a domain by number. The selection is validated
to ensure it is a valid integer and within the range of available options.
This prevents invalid list access and runtime errors.

If a valid selection is made, the corresponding password is displayed in a
controlled, formatted manner and the retrieval action is logged. Appropriate
error messages are shown for invalid input, missing users, or empty password
lists.
"""

def update_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Check if the user exists and has stored passwords
    if uid in app_password and app_password[uid]:
        print("="*40)
        print(f"{'Stored Passwords'.center(40)}")  # Title centered
        print("="*40)

        # Enumerate through the list of stored passwords and display the domains
        for index, entry in enumerate(app_password[uid], 1):
            print(f"{index}. {entry['domain']}")  # Display domain name

        # Allow the user to select an option to update a specific password
        try:
            choice = int(input("\nEnter the option number to update the password: "))

            # Validate if the choice is within the valid range
            if 0 < choice <= len(app_password[uid]):
                selected_entry = app_password[uid][choice - 1]

                # Prompt the user for the new password
                print(f"<======  If you wish to generate a random password, leave the password field as blank. ======>")
                new_password = input(f"Enter the new password for {selected_entry['domain']}: ")

                # Generating a random password if the user has not provided the password and updating it
                # Generating a random password if the user has not provided the password and updating it
                if new_password == "":
                    selected_entry["pwd"] = generate_secure_password()
                else:
                    selected_entry["pwd"] = new_password

                # Write the updated passwords back to the file
                write_passwords(app_password)

                # Log the password update
                log_update(f"Updated password for {selected_entry['domain']} under user {uid}")

                # Provide success feedback to the user
                print("*"*40)
                print(f"Password for {selected_entry['domain']} updated successfully.")
                print("*"*40)

            else:
                    # Handle invalid selection
                print("\n[!] Invalid option selected. Please choose a valid number.\n")

        except ValueError:
                # Handle non-integer input
                print("\n[!] Please enter a valid number.\n")

    else:
            # If no passwords are stored or user is not found
            print("\n[!] No passwords stored or user not found.\n")
def delete_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Check if the user exists and has stored passwords
    if uid in app_password and app_password[uid]:
        print("=" * 40)
        print(f"{'Stored Passwords'.center(40)}")
        print("=" * 40)

        # Enumerate through the list of stored passwords and display the domains
        for index, entry in enumerate(app_password[uid], 1):
            print(f"{index}. {entry['domain']}")

        try:
            choice = int(input("\nEnter the option number to delete the password: "))
            if 0 < choice <= len(app_password[uid]):
                deleted_entry = app_password[uid].pop(choice - 1)  # Delete the entry

                write_passwords(app_password)  # Update the password file

                log_update(f"Deleted password for {deleted_entry['domain']} under user {uid}")
                log_update(f"Deleted credentials - user: {uid}, domain: {deleted_entry['domain']}, password: {deleted_entry['pwd']} ")

                print("*" * 40)
                print(f"Password for {deleted_entry['domain']} deleted successfully.")
                print("*" * 40)

            else:
                print("\n[!] Invalid option selected. Please choose a valid number.\n")

        except ValueError:
            print("\n[!] Please enter a valid number.\n")
    else:
        print("\n[!] No passwords stored or user not found.\n")


def main():

    if os.path.exists("master_login.json"):
        with open("master_login.json", 'r') as file:
            master_login = json.load(file)


    while True:
        # Create a more visually appealing header
        print("="*40)
        print(f"{'Welcome to the Password Manager'.center(40)}")
        print("="*40)

        # User login
        uid = input("Enter your UID: ")
        if uid not in master_login:
            print("\n[!] User not found.\n")
            continue

        pss = input("Enter your password: ")
        if master_login[uid] != pss:
            print("\n[!] Password mismatch.\n")
            continue

        # updating the log for an user login
        log_update(f"User {uid} has logged-in")

        # Success message with stylized heading
        print("*"*40)
        print(f"{f'Login successful - Welcome {uid}'.center(40)}")
        print("*"*40)

        # Menu for actions
        while True:
            print("\nSelect an option:")
            print("+"*40)
            print("1. Add Password")
            print("2. Retrieve Password")
            print("3. Update Password")
            print("4. Delete Password")
            print("9. Exit")
            print("+"*40)

            choice = input("Choose an option: ")

            if choice == "1":
                add_password(uid)
            elif choice == "2":
                retrieve_password(uid)
            elif choice == "3":
                update_password(uid)
            elif choice == "4":
                delete_password(uid)
            elif choice == "9":
                print(f"\n[!] Exiting the Password Manager. Stay safe! - {uid}")
                break
            else:
                print("\n[!] Invalid option. Please try again.\n")

        # End message
        print("="*40)
        print(f"{'Thank you for using the Password Manager!'.center(40)}")
        print("="*40)
        break  # Break the while loop to exit after finishing tasks.

if __name__ == "__main__":
    main()
