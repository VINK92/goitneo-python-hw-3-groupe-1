from error_decorator import input_error


def hello_command():
    return "How can I help you?"


@input_error
def add_contact_command(username, phone, contacts):
    contacts[username] = phone
    return f"Contact {username} with phone number {phone} added successfully."


@input_error
def change_phone_command(username, phone, contacts):
    if username in contacts:
        contacts[username] = phone
        return f"Phone number for contact {username} changed successfully."
    else:
        return f"Contact {username} does not exist."


@input_error
def phone_command(username, contacts):
    if username in contacts:
        return f"The phone number for contact {username} is {contacts[username]}."
    else:
        return f"Contact {username} does not exist."


@input_error
def all_command(contacts):
    if contacts:
        return "\n".join([f"{username}: {phone}" for username, phone in contacts.items()])
    else:
        return "No contacts found."


def bot():
    contacts = {}
    while True:
        command = input("Enter a command: ").strip().lower()
        if command == "close" or command == "exit":
            print("Good bye!")
            break
        elif command == "hello":
            print(hello_command())
        elif command.startswith("add"):
            split_command = command.split(maxsplit=2)
            if len(split_command) < 3:
                print("Invalid input format. Please provide both username and phone number.")
                continue
            _, username, phone = split_command
            print(add_contact_command(username, phone, contacts))
        elif command.startswith("change"):
            split_command = command.split(maxsplit=2)
            if len(split_command) < 3:
                print("Invalid input format. Please provide both username and phone number.")
                continue
            _, username, phone = split_command
            print(change_phone_command(username, phone, contacts))
        elif command.startswith("phone"):
            split_command = command.split(maxsplit=1)
            if len(split_command) < 2:
                print("Enter a valid username.")
                continue
            _, username = split_command
            print(phone_command(username, contacts))
        elif command == "all":
            print(all_command(contacts))
        else:
            print("Invalid command. Please try again.")


bot()
