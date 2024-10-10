# Generates a random 32-character hex string
# to be used as the Flask secret key
#
# Usage:
# python generate_flask_secret.py
#
# Output:
# 5b4f2b1e7d0f9b1e7d0f9b1e7d0f9b1e
#
# Note: The output will be different each time you run the script
#
# Reference:
# https://docs.python.org/3/library/secrets.html
#

import secrets

secret_key = secrets.token_hex(16)

print(secret_key)
