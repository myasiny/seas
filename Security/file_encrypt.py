from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

encrypted = cipher.encrypt("Test")

decrypted = cipher.decrypt(encrypted)