from cryptography.fernet import Fernet
import audible

# Encrypt the password
# Generate and store a key (do this once, securely)
key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)

# Encrypt and save the password
cipher_suite = Fernet(key)
encrypted_password = cipher_suite.encrypt(b"yourpassword")
with open("auth_credentials.enc", "wb") as file:
    file.write(encrypted_password)

from cryptography.fernet import Fernet

# Load the key
with open("key.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

# Decrypt the password
with open("auth_credentials.enc", "rb") as file:
    encrypted_password = file.read()
PASSWORD = cipher_suite.decrypt(encrypted_password).decode()
    





auth = audible.Authenticator.from_login("USERNAME", "PASSWORD", locale="COUNTRY_CODE")
auth.to_file("auth_credentials.json")  # Save credentials for reuse
