from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from argon2 import PasswordHasher
import argon2

class Secure:
    def __init__(self):
        self.key = get_random_bytes(16)
        self.iv = get_random_bytes(16)

    def get_key(self):
        return self.key

    def get_iv(self):
        return self.iv

    def set_key(self, key):
        self.key = key

    def set_iv(self, iv):
        self.iv = iv

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(pad(data, AES.block_size))

    def decrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(data), AES.block_size)


# Argon 2 
# The Password Hashing Competition took place between 2012 and 2015 
# to find a new, secure, and future-proof password hashing algorithm. 
# In the end, Argon2 was announced as the winner.

# Argon2 is a secure password hashing algorithm. 
# It is designed to have both a configurable runtime as well as memory consumption.
# This means that you can decide how long it takes to hash a password and how much memory is required.
class Argon2:
    def __init__(self):
        # Uses Argon2id by default and always uses a random salt for hashing. 
        # But it can verify any type of Argon2 as long as the hash is correctly encoded.
        self.ph = PasswordHasher(time_cost=1, memory_cost=1024, hash_len=32)
        self.hashed = None

    def get_hash(self):
        return self.hashed

    def hash(self, password):
        try:
            self.hashed = self.ph.hash(password)
            return self.hashed

        except argon2.exceptions.HashingError:
            print("Hashing failed")

    def verify(self, password, hash):
        try:
            return self.ph.verify(hash, password)
        
        except argon2.exceptions.VerificationError:
            print("Verification failed")

        except argon2.exceptions.InvalidHash:
            print("Invalid hash")


# if __name__ == "__main__":
#     s = Secure()
#     print(f"key: {s.get_key()}")
#     print(f"iv: {s.get_iv()}")
#     print("message: Hello World!  encrypted message:", s.encrypt(b"Hello World!"))
#     print("dencrypted message:",s.decrypt(s.encrypt(b"Hello World!")))

#     a = Argon2()
#     hash = a.hash('correct horse battery staple')
#     print(type(hash), len(hash), hash, '\n')
#     print(a.get_hash())
#     print(f"verify: {a.verify('correct horse battery staple', hash)}")
