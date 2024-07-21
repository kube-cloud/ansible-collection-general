# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from base64 import b64encode
from ..module_utils.commons import generate_random_string


try:
    from passlib.hash import pbkdf2_sha512
    from passlib.utils.binary import ab64_decode
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Define Hash Function
def pbkdf2_hash(password: str, salt: str = '', rounds: int = 100000):

    # Check Passord Key
    if not password or password.strip() == '':

        # Raise Error
        raise ValueError("The Field 'password' is Mandatory.")

    # Check Salt
    if salt.strip() == '':

        # Define Random SALT
        salt = generate_random_string(
            length=16
        )

    # Check Rounds
    if rounds <= 0:

        # Define Default Rounds
        rounds = 100000

    # Build Hash Array
    hash_array = pbkdf2_sha512.hash(password, salt=salt.encode(), rounds=rounds).split('$')

    # Compute Encoded Salt
    salt_encoded = b64encode(ab64_decode(hash_array[3])).decode()

    # Compute Encoded Password
    password_encoded = b64encode(ab64_decode(hash_array[4])).decode()

    # Build Single Line Password
    password_single_line = "${prolog}${rounds}${salt_encoded}${password_encoded}".format(
        prolog="pbkdf2-sha512",
        rounds=rounds,
        salt_encoded=salt_encoded,
        password_encoded=password_encoded
    )

    # Create and return Transaction
    return {
        "password_original": password,
        "salt_original": salt,
        "salt": salt_encoded,
        "password_single_line": password_single_line,
        "password_crypted": password_single_line.split('$')[2] + '$' + password_encoded,
        "rounds": password_single_line.split('$')[2],
        "hash_method": "PBKDF2",
        "hash_algoritm": "SHA512"
    }


# Filter Module Class
class FilterModule(object):

    # Define Filter
    def filters(self):

        # Return Filter Method
        return {
            'pbkdf2_hash': pbkdf2_hash,
        }
