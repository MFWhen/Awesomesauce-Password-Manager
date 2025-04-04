from cryptography.fernet import Fernet
import base64
import os
import getpass
import json
import hashlib




def generate_key(master_password):
    return base64.urlsafe_b64encode(master_password.encode().ljust(32)[:32])


def save_master_password(master_password):
    key = generate_key(master_password)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(master_password.encode())
    with open("master_password.txt", "wb") as file:
        file.write(encrypted_password)


def load_and_verify_master_password():
    master_password = getpass.getpass("Enter master password: ")
    key = generate_key(master_password)
    cipher = Fernet(key)

    try:
        with open("master_password.txt", "rb") as file:
            encrypted_password = file.read()
        saved_password = cipher.decrypt(encrypted_password).decode()
        return master_password == saved_password, key
    except Exception:
        return False, None


def create_master_password():
    while True:
        print("No master password found. Please create one.")
        master_password = getpass.getpass("Create master password: ")
        confirm_password = getpass.getpass("Confirm master password: ")

        if master_password == confirm_password:
            save_master_password(master_password)
            print("Master password created and saved successfully.")
            break
        else:
            print("Passwords do not match. Please start over.")


def check_master_password():
    if not os.path.exists("master_password.txt"):
        create_master_password()


def add_password(key):
    cipher = Fernet(key)
    account_type = input("Enter account type (e.g., Facebook, Twitter): ")
    username = input(f"Enter username/email for {account_type}: ")
    password = getpass.getpass(f"Enter password for {username} on {account_type}: ")

    encrypted_password = cipher.encrypt(password.encode())

    with open("passwords.txt", "a") as file:
        file.write(f"{account_type}:{username}:{encrypted_password.decode()}\n")

    print("Password added successfully!")


def view_passwords(key):
    cipher = Fernet(key)

    try:
        with open("passwords.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                print("No passwords found.")
                return

            account_types = {i + 1: line.split(":")[0] for i, line in enumerate(lines)}
            print("Available account types:")
            for i, account_type in account_types.items():
                print(f"{i}. {account_type}")

            choice = int(input("Choose an account type by number: "))
            if choice not in account_types:
                print("Invalid choice.")
                return

            selected_line = lines[choice - 1].strip()
            account_type, username, encrypted_password = selected_line.split(":")
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()

            print(f"\nAccount: {account_type}\nUsername: {username}\nPassword: {decrypted_password}\n")
    except FileNotFoundError:
        print("No passwords found. Please add some passwords first.")


def delete_password(key):
    cipher = Fernet(key)

    try:
        with open("passwords.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                print("No passwords to delete.")
                return

            account_types = {i + 1: line.split(":")[0] for i, line in enumerate(lines)}
            print("Available account types for deletion:")
            for i, account_type in account_types.items():
                print(f"{i}. {account_type}")

            choice = int(input("Choose an account type to delete by number: "))
            if choice not in account_types:
                print("Invalid choice.")
                return

            with open("passwords.txt", "w") as file:
                for i, line in enumerate(lines):
                    if i != choice - 1:
                        file.write(line)

            print("Password deleted successfully!")
    except FileNotFoundError:
        print("No passwords found. Please add some passwords first.")

incorrectMessage='Incorrect Password.'
greeting='Welcome to Awesomesauce Password Manager!'


def load_custom_messages():
    global incorrectMessage, greeting
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as file:
            config = json.load(file)
            incorrectMessage = config.get("incorrectMessage", incorrectMessage)
            greeting = config.get("greeting", greeting)


def save_custom_messages():
    config = {
        "incorrectMessage": incorrectMessage,
        "greeting": greeting
    }
    with open("config.txt", "w") as file:
        json.dump(config, file)

def customMessages():
    global greeting, incorrectMessage
    print("1. Main Menu Greeting")
    print("2. Invalid Password Message")
    print("0. Return to Settings")
    choice = int(input("Which of these would you like to customize?: "))
    
    if choice == 1:
        greeting = input("Please enter your main menu greeting: ")
        save_custom_messages()  
    elif choice == 2:
        incorrectMessage = input("Please enter the message to be shown when user inputs wrong password: ")
        save_custom_messages()  
    elif choice == 0:
        settings()
    else:
        print("Invalid Choice")

def settings():
    print("1. Custom Messages")
    print("2. Max Password Atempts")
    print("0. Return to Main Menu")

    choice=int(input("Choose an option: "))
    if choice == 1:
        customMessages()
    elif choice == 0:
        main()
    else:
        print("Invalid Choice")
       
        


def main():
    load_custom_messages()
    check_master_password()
    is_verified, key = load_and_verify_master_password()
    if not is_verified:
        #load_custom_messages() [WIP feature]
        print(incorrectMessage)
        return

    while True:
        #load_custom_messages() [WIP feature]
        print(greeting)
        print("1. Add a new password")
        print("2. View stored passwords")
        print("3. Delete a password")
        print("4. Settings (WORK IN PROGRESS!)")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_password(key)
        elif choice == '2':
            view_passwords(key)
        elif choice == '3':
            delete_password(key)
        elif choice == '4':
            settings()
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
