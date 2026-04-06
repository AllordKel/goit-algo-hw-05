import re


def normalize_phone(phone_number: str) -> str:
    """
    Puts phone number in +38########## format.
    Keeps initial country code if exists.
    Adds "+38" if no country code.
    """

    if type(phone_number) != str:  # trying to convert invalid data type
        try:
            phone_number = str(phone_number)
        except TypeError:
            return phone_number

    modified_number = re.sub(r"[^\d\+]", "", phone_number)  # removing all nondigit and non "+" symbols
    modified_number = re.sub(r"(?<!^)\+", "", modified_number)  # removing all extra "+" except of first just in case
    if modified_number.startswith("+"):
        return modified_number
    elif modified_number.startswith("38"):
        return "+" + modified_number
    else:
        return "+38" + modified_number
