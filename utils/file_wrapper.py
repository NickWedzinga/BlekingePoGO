import os

from utils.exception_wrapper import catch_with_print


def found_in_file(str_to_find: str, file_name: str):
    """
    Attempts to find str_to_find in file_name.
    If found; the entry (that line) is returned, else False is returned.
    """
    with open(file_name) as file:
        for entry in file:
            if str_to_find.lower() in entry.lower():
                return entry
    return False


def append_to_file(str_to_add: str, file_name: str):
    """
    Appends the provided String to the provided file on a new line.
    """
    with open(file_name, "a") as file:
        file.write(str_to_add + "\n")


def remove_line_from_file(str_to_remove: str, file_name: str):
    """
    Removes the line with the provided String from the provided file
    """
    removed = False
    with open(file_name, "r") as f:
        lines = f.readlines()
    with open(file_name, "w") as f:
        for line in lines:
            if str_to_remove not in line:
                f.write(line)
            else:
                removed = True
    return removed


async def create_file(file_name: str):
    """Created a file with the provided file_name"""
    await catch_with_print(open, "create_file", file_name, "x")


def delete_file(file_to_delete: str):
    """Deleted the provided file"""
    os.remove(file_to_delete)
