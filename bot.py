from error_decorator import input_error
from main import AddressBook, Record


def hello_command():
    return "How can I help you?"


@input_error
def add_contact_command(username, phone, contacts):
    new_contact = Record(username)
    new_contact.add_phone(phone)
    contacts.add_record(new_contact)
    return f"Contact {username} with phone number {phone} added successfully."


@input_error
def change_phone_command(username, old_phone, new_phone, contacts):
    record = contacts.find(username)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for contact {username} changed successfully."
    else:
        return f"Contact {username} does not exist."


@input_error
def phone_command(username, contacts):
    record = contacts.find(username)
    if record:
        phones = ", ".join(str(phone) for phone in record.phones)
        return f"The phone number for contact {username} is {phones}."
    else:
        return f"Contact {username} does not exist."


@input_error
def all_command(contacts):
    if len(contacts.data.values()) > 0:
        contact_list = ""
        for record in contacts.data.values():
            contact_list += str(record) + "\n"
        return contact_list
    else:
        return "No contacts found."


@input_error
def add_birthday(name, birthday, contacts):
    record = contacts.find(name)
    if record:
        if record.birthday:
            return f"Contact {name} already has a birthday ({record.birthday})."
        else:
            record.add_birthday(birthday)
            return f"Birthday added for {name}: {birthday}"
    else:
        return f"Contact {name} not found."


@input_error
def show_birthday(name, contacts):
    record = contacts.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday: {record.birthday}"
        else:
            return f"{name} does not have a birthday set."
    else:
        return f"Contact {name} not found."


@input_error
def birthdays(contacts):
    return contacts.get_birthdays_per_week()


def bot():
    contacts = AddressBook()
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
            split_command = command.split(maxsplit=3)
            if len(split_command) < 4:
                print("Invalid input format. Please provide both username and phone number.")
                continue
            _, username, old_phone, new_phone = split_command
            print(change_phone_command(username, old_phone, new_phone, contacts))
        elif command.startswith("phone"):
            split_command = command.split(maxsplit=1)
            if len(split_command) < 2:
                print("Enter a valid username.")
                continue
            _, username = split_command
            print(phone_command(username, contacts))
        elif command == "add-birthday":
            split_command = command.split(maxsplit=3)
            _, username, birthday = split_command
            print(add_birthday(username, birthday, contacts))
        elif command == "show-birthday":
            split_command = command.split(maxsplit=1)
            _, username = split_command
            print(show_birthday(username, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        elif command == "all":
            print(all_command(contacts))
        else:
            print("Invalid command. Please try again.")


bot()

# change Iryna 0949332809 0939491111
# add Vika 0939493809
# add-birthday vika 10.12.1992
# change vika 0939493809 0949332809
# add Iryna 0949332809