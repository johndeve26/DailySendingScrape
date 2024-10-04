import random
import string


def generate_unique_code(length=10):
    # Define the character pool (uppercase, lowercase, digits, and special characters)
    characters = string.ascii_letters + string.digits + string.punctuation  # Includes !@#$%^&*()_+...

    # Ensure we have enough unique characters to generate the code
    if length > len(characters):
        raise ValueError("Length exceeds available unique characters.")

    # Randomly sample unique characters from the pool
    unique_code = ''.join(random.sample(characters, length))
    return unique_code

