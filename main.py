import pickle
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Date should be in format DD.MM.YYYY")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.is_valid(value):
            raise ValueError("Invalid phone number format.")

    @staticmethod
    def is_valid(value):
        return len(value) == 10 and value.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None  # Замість self.birthday = ""
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}"

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def show_birthday(self):
        return self.birthday

    def days_to_birthday(self):
        if not self.birthday:
            return None
        bday = datetime.strptime(self.birthday.value, '%d.%m.%Y')
        now = datetime.now()
        next_bday = bday.replace(year=now.year)
        if next_bday < now:
            next_bday = next_bday.replace(year=now.year + 1)
        return (next_bday - now).days

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.now()
        result = {}
        for name, record in self.data.items():
            days = record.days_to_birthday()
            if days is not None and 0 <= days <= 7:
                weekday = (today + timedelta(days=days)).strftime('%A')
                result.setdefault(weekday, []).append(name)
        return result

    def add_birthday(self, name, date):
        record = self.find(name)
        if record:
            record.add_birthday(date)
        else:
            print("Contact not found.")

    def show_birthday(self, name):
        record = self.find(name)
        if record and record.birthday:
            print(f"{name}'s birthday: {record.birthday}")
        elif record:
            print(f"{name} does not have a birthday.")
        else:
            print("Contact not found.")

    def birthdays(self):
        birthdays_list = self.get_birthdays_per_week()
        if birthdays_list:
            print("Birthdays for the next week:")
            for weekday, names in birthdays_list.items():
                print(f"{weekday}: {', '.join(names)}")
        else:
            print("No birthdays for the next week.")

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

if __name__ == "__main__":
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    jane_record.add_birthday('12.12.2000')

    for record in book.data.values():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")

    jane_record.add_birthday('15.03.2024')
    book.birthdays()
