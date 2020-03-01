"""
Utility functions used by any app.
"""

import string
import random


def generate_unique_model_id(model_class, prefix, variable_part_length):
    """Generates an alphanumeric model ID that's not present in the database.

    Args:
        model_class: Class object of the model which will be used to check if
                     the id already exists.
        prefix: String prefix to which an ID will be appended.
        variable_part_length: Length of the ID succeeding the prefix.

    Returns:
        Generated alphanumeric ID.

    """
    while True:
        unique_alphanum = generate_random_alphanumeric(variable_part_length)
        unique_id = f'{prefix}{unique_alphanum}'
        if not model_class.objects.filter(string_id=unique_id).exists():
            return unique_id


def generate_random_alphanumeric(length):
    """Creates a random alphanumeric string.

    Args:
        length: Desired length of the output string.

    Returns:
        Generated alphanumeric string.

    """
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(length))
