import random
import string
from datetime import date

def generate_ticket_number():
    # Generate a random string of uppercase letters and digits
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Concatenate the random string with the current year
    ticket_number = f'{random_string}-{date.today().year}'

    return ticket_number
