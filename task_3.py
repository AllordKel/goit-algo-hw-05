from sys import argv, exit
from pathlib import Path
import re


def parse_log_line(line: str) -> dict:
    """
    Creates a dictionary from a line from logs.
    Expects data in line to be in format: yyyy-mm-dd hh:mm:ss log_level messege.
    Does not process and informs about bad data format in line.

    Dictionary keys:
        date
        time
        type
        messege
    """

    splitted_line = line.split()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", splitted_line[0]):
        print(f"Bad date format in line {line}")  # date format validation
        exit(1)
    elif not re.match(r"^\d{2}:\d{2}:\d{2}$", splitted_line[1]):
        print(f"Bad time format in line {line}")  # time format validation
        exit(1)
    elif splitted_line[2] not in ["INFO", "DEBUG", "ERROR", "WARNING"]:
        print(f"Unknown log type in line {line}")  # log format validation
        exit(1)
    else:
        dict = {"date": splitted_line[0], "time": splitted_line[1], "type": splitted_line[2], "messege": " ".join(splitted_line[3:])}
        return dict


def load_logs(file_path: str) -> list:
    """
    Validates if povided path leads to axisting log file.
    Reads from log file and returns a list of dictionaries with log data by row.
    """

    log_file_path = Path(file_path)

    if not log_file_path.is_file():  # File validation
        print("Invalid file or path to file, path should lead to log file that exists")
        exit(1)

    with open(file_path, "r", encoding="utf-8") as file:
        return [parse_log_line(line.strip()) for line in file.readlines()]  # List comprehension


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Returns filtered by specific log type list of dictionaries with logs.
    """

    return list(filter(lambda log: log["type"] == level, logs))  # lambda function and filter function


def count_logs_by_level(logs: list) -> dict:
    """
    Counts how many of each log type in the file.
    Returns a dictionary where keys are log type name and values are the freequency of meeting in the file.
    Also if additional instruction of specific log level provided -
    uses filter_logs_by_level function to filter those logs and write it to the dictionary with keys of numbers from 0
    and values - dictionaries of the required logs.

    Dictionary keys:
        INFO
        DEBUG
        ERROR
        WARNING
    if details by log level were requested:
        0
        1
        2
        depending of how many required logs of a type.
    """
    levels_dict = {}
    levels = ["INFO", "DEBUG", "ERROR", "WARNING"]
    specific_log_level = argv[2].upper() if len(argv) > 2 and argv[2].upper() in levels else ""  # If additional instruction provided, saves it in specific_log_level
    for level in levels:
        filtered_logs = filter_logs_by_level(logs, level)  # saves result of filter_logs_by_level function to variable for particular log type/level.
        levels_dict[level] = len(filtered_logs)  # Creates a key with level name and gives it a number value of lenth of filtered log list.

        if level == specific_log_level:  # If log level is the one specified with the file call.
            for i in range(len(filtered_logs)):
                levels_dict[i] = filtered_logs[i]  # Creates a key of numbers from 0 to lenth of filtered log list and gives each of those number keys a specified filtered log dictionary.

    return levels_dict


def display_log_counts(counts: dict):
    """
    Prints all gathered data in console/terminal
    """
    print(f"{'Рівень логування':<17} | {'Кількість':<10}")
    print(f"{'-'*17}-|-{'-'*10}")
    for level, count in counts.items():
        if level in ["INFO", "DEBUG", "ERROR", "WARNING"]:
            print(f"{level:<17} | {count:<10}")
    if len(counts) > 4:  # If lenth of dictionary with counts is bigger then the number of log types - means there was a specific request by log level/type as well since now dictionary have additional number keys with filtered logs.
        log_level = argv[2].upper()
        print()
        print(f"Деталі логів для рівня '{log_level}':")
        for i in range(len(counts) - 4):  # number of those additional logs would be lenth of dictionary extracting four initial log types.
            print(f"{counts[i]['date']} {counts[i]['time']} - {counts[i]['messege']}")


try:
    display_log_counts(count_logs_by_level(load_logs(argv[1])))
except IndexError:
    print("Log file path is expected.")
    exit(1)

if __name__ == "__main__":
    # python task_3.py task_3_test.txt - For testing purpose.
    pass
