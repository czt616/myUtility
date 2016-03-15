"""
define Exceptions
"""

class TooManyInput(Exception):
        def __init__(self):
            pass
        def __str__(self):
            error_message = "Too many inputs\n"
            return error_message


