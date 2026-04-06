from pathlib import Path
from normalize_phone_3 import normalize_phone


def add_input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner


def change_input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner


def parse_input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "", ""

    return inner


def phone_input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Give me a name please."
        except KeyError:
            return "Contact not found"
        
    return inner


@parse_input_error
def parse_input(user_input):
    """Normalize input into command and positional arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def load_file(path="contacts.txt"):
    """Load contacts from a plain text file as a dictionary.

    The file format is one contact per line:
        name:phone
    """
    p = Path(path)
    if not p.exists():
        return {}  # File may not exist on first run; return an empty phonebook

    contacts = {}
    with open(p, "r", encoding="utf-8") as fh:
        lines = [el.strip() for el in fh.readlines()]

    for line in lines:
        if not line or ":" not in line:
            continue  # Skip empty or malformed lines
        name, phone = line.split(":")
        contacts[name.strip()] = phone.strip()
    return contacts


def save_file(contacts, path="contacts.txt"):
    """Save contacts dictionary to a plain text file."""
    with open(Path(path), "w", encoding="utf-8") as phone_directory:
        for name, phone in contacts.items():
            phone_directory.write(f"{name}:{phone}\n")


@add_input_error
def add_contact(args):
    contacts = load_file()
    name, phone = args
    if name.lower() in contacts:
        return "Such contact already exists"
    contacts[name.lower()] = normalize_phone(phone)
    save_file(contacts)
    return "Contact added."


@change_input_error
def change_contact(args):
    contacts = load_file()
    name, phone = args
    if name.lower() not in contacts:
        return "No contact found"
    contacts[name.lower()] = normalize_phone(phone)
    save_file(contacts)
    return "Contact updated."


def show_all():
    """Display all contacts or a specific message when phonebook is empty."""
    contacts = load_file()
    if not contacts:
        return "Phonebook is empty, save some contacts first"

    output = []
    for name, phone in contacts.items():  # Returning all contacts
        output.append(f"{name}: {phone}")
    return "\n".join(output)


@phone_input_error
def show_phone(args):
    """Retrieve the phone number for a specific contact."""
    contacts = load_file()
    return contacts[args[0].lower()]


def main():
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("Hello, how can I help you?")

        elif command == "add":
            print(add_contact(args))

        elif command == "change":
            print(change_contact(args))

        elif command == "phone":
            print(show_phone(args))

        elif command == "all":
            print(show_all())

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
