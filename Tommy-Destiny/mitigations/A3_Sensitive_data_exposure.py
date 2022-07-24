import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

class AES_GCM:
    def __init__(self):
        self.HASH_NAME = "SHA512"
        self.IV_LENGTH = 12
        self.ITERATION_COUNT = 65536
        self.KEY_LENGTH = 32
        self.SALT_LENGTH = 16
        self.TAG_LENGTH = 16
        self.key = None

    def get_iv(self):
        return get_random_bytes(self.IV_LENGTH)

    def get_key(self):
        return self.key

    def encrypt(self, password, plain_message):
        salt = get_random_bytes(self.SALT_LENGTH)
        key = self.get_secret_key(password, salt)
        self.key = key

        iv = self.get_iv()
        cipher = AES.new(key, AES.MODE_GCM, iv)

        encrypted_message_byte, tag = cipher.encrypt_and_digest(plain_message)
        cipher_byte = iv + salt + encrypted_message_byte + tag

        encoded_cipher_byte = base64.b64encode(cipher_byte)
        return bytes.decode(encoded_cipher_byte)

    def decrypt(self, password, cipher_message):
        decoded_cipher_byte = base64.b64decode(cipher_message)

        iv = decoded_cipher_byte[:self.IV_LENGTH]
        salt = decoded_cipher_byte[self.IV_LENGTH:(self.IV_LENGTH + self.SALT_LENGTH)]
        encrypted_message_byte = decoded_cipher_byte[(self.IV_LENGTH + self.SALT_LENGTH):-self.TAG_LENGTH]
        tag = decoded_cipher_byte[-self.TAG_LENGTH:]

        key = self.get_secret_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, iv)

        decrypted_message_byte = cipher.decrypt_and_verify(encrypted_message_byte, tag)
        return decrypted_message_byte.decode("utf-8")

    def get_secret_key(self, password, salt):
        return hashlib.pbkdf2_hmac(self.HASH_NAME, password.encode(), salt, self.ITERATION_COUNT, self.KEY_LENGTH)


from argon2 import PasswordHasher, Type, exceptions

# provides a balanced approach to resisting both side-channel and GPU-based attacks
# Argon2id should use one of the following configuration settings as a base minimum which includes 
# the minimum memory size (m), the minimum number of iterations (t) and the degree of parallelism (p).
# m=37 MiB, t=1, p=1

class Argon2ID:
    def __init__(self):
        self.hasher = PasswordHasher(time_cost=2, memory_cost=1024, parallelism=1, type=Type.ID)

    def hash_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, hash, password):
        try:
            return self.hasher.verify(hash, password)
        except exceptions.VerifyMismatchError:
            return "The secret does not match the hash"


# if __name__ == "__main__":
#     AES_GCM = AES_GCM()
#     outputFormat = "{:<25}:{}:{}"
#     secret_key = "yourSecretKey"
#     plain_text = "Hello how are yo doing"

#     print("------ AES-GCM Encryption ------")
#     cipher_text = AES_GCM.encrypt(secret_key, plain_text)
#     # print(AES_GCM.get_key())
#     # print(AES_GCM.get_iv())
#     # print(outputFormat.format("encryption input", plain_text, type(plain_text)))
#     # print(outputFormat.format("encryption output", cipher_text, type(cipher_text)))

#     # decrypted_text = AES_GCM.decrypt(secret_key, cipher_text)

#     # print("\n------ AES-GCM Decryption ------")
#     # print(outputFormat.format("decryption input", cipher_text, type(plain_text)))
#     # print(outputFormat.format("decryption output", decrypted_text, type(plain_text)))

#     print("\n------ Argon2ID Hashing Algorithm ------")
#     hasher = Argon2ID()
#     password = "password"

#     hash = hasher.hash_password(password)
#     print(hash)
#     print(hasher.verify_password(hash, password))