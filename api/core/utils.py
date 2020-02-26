import string
import random


def generate_unique_model_id(model_class, prefix, variable_part_length):
    while True:
        unique_alphanum = generate_random_alphanumeric(variable_part_length)
        unique_id = f'{prefix}{unique_alphanum}'
        if not model_class.objects.filter(string_id=unique_id).exists():
            return unique_id


def generate_random_alphanumeric(length):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(length))
