"""Utility functions for changing the files in the repository."""

import os
import re

from config import TARGET_DIR

def change(func):
    """Changes all files in the repository using the text changing function
    `func`."""
    for file_name in os.listdir(TARGET_DIR):
        target = os.path.join(TARGET_DIR, file_name)
        if os.path.isfile(target) and file_name.endswith(".mw"):
            with open(target, "r") as file_handler:
                source = file_handler.read()

            with open(target, "w") as file_handler:
                file_handler.write(func(source))

def regex_change(regex, match, flags=0):
    """Changes all files in the repository using `re.sub()`."""
    change(lambda x: re.sub(regex, match, x, flags=flags))
