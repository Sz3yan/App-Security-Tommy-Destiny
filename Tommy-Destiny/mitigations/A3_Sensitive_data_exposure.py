from google.cloud import kms
from google.protobuf import duration_pb2
import os
import datetime
import crcmod
import six
import time
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


class GoogleCloudKeyManagement:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sz3yan/Tommy-Destiny/Tommy-Destiny/google.json"

    # create once only when setup
    def create_key_ring(self, project_id, location_id, key_ring_id):
        client = kms.KeyManagementServiceClient()
        location_name = f'projects/{project_id}/locations/{location_id}'

        key_ring = {}

        created_key_ring = client.create_key_ring(
            request={'parent': location_name, 'key_ring_id': key_ring_id, 'key_ring': key_ring})
        print('Created key ring: {}'.format(created_key_ring.name))
        return created_key_ring


    def create_key_rotation_schedule(self, project_id, location_id, key_ring_id, key_id):
        client = kms.KeyManagementServiceClient()

        key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)

        purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
        algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
        key = {
            'purpose': purpose,
            'version_template': {
                'algorithm': algorithm,
            },

            # Rotate the key every 30 days.
            'rotation_period': {
                'seconds': 60 * 60 * 24 * 30
            },

            # Start the first rotation in 24 hours.
            'next_rotation_time': {
                'seconds': int(time.time()) + 60 * 60 * 24
            }
        }

        created_key = client.create_crypto_key(
            request={'parent': key_ring_name, 'crypto_key_id': key_id, 'crypto_key': key})
        print('Created labeled key: {}'.format(created_key.name))
        return created_key

    
    def create_key(self, project_id, location_id, key_ring_id, key_id):
        client = kms.KeyManagementServiceClient()

        # Build the parent key ring name.
        key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)

        # Build the key.
        purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
        algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
        key = {
            'purpose': purpose,
            'version_template': {
                'algorithm': algorithm,
            }
        }

        # Call the API.
        created_key = client.create_crypto_key(
            request={'parent': key_ring_name, 'crypto_key_id': key_id, 'crypto_key': key})
        print('Created labeled key: {}'.format(created_key.name))
        return created_key

    def retrieve_key(self, project_id, location_id, key_ring_id, key_id):
        client = kms.KeyManagementServiceClient()

        key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
        retrieved_key = client.get_crypto_key(request={'name': key_name})
        # print('Retrieved key: {}'.format(retrieved_key.name))
        return retrieved_key

    def update_key(self, project_id, location_id, key_ring_id, key_id):
        client = kms.KeyManagementServiceClient()

        # Build the parent key ring name.
        key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)

        # Build the key.
        purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
        algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
        key = {
            'purpose': purpose,
            'version_template': {
                'algorithm': algorithm,
            }
        }

        # Call the API.
        updated_key = client.update_crypto_key(
            request={'crypto_key': key, 'name': key_name})
        print('Updated key: {}'.format(updated_key.name))
        return updated_key


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

class Argon2ID:
    """
        provides a balanced approach to resisting both side-channel and GPU-based attacks
        Argon2id should use one of the following configuration settings as a base minimum which includes 
        the minimum memory size (m), the minimum number of iterations (t) and the degree of parallelism (p).
        m=37 MiB, t=1, p=1
    """
    def __init__(self):
        self.hasher = PasswordHasher(time_cost=2, memory_cost=1024, parallelism=1, type=Type.ID)

    def hash_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, hash, password):
        try:
            return self.hasher.verify(hash, password)
        except exceptions.VerifyMismatchError:
            return "The secret does not match the hash"


# if __name__ == '__main__':
#     # create_key_ring = create_key_ring("tommy-destiny", "global", "my-key-ring")
#     # create_key_asymmetric_sign("tommy-destiny", "global", "my-key-ring", "my-asymmetric-signing-key")
#     # create_key_asymmetric_decrypt("tommy-destiny", "global", "my-key-ring", "my-asymmetric-decrypt-key")
    
    # import os
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sz3yan/Tommy-Destiny/google.json"

    # a = GoogleCloudKeyManagement()
    # # a.create_key_rotation_schedule("tommy-destiny", "global", "my-key-ring", "key-rotation")
    # # a.update_key_add_rotation("tommy-destiny", "global", "my-key-ring", "key-rotation")

    # print(a.retrieve_key("tommy-destiny", "global", "my-key-ring", "key-rotation"))

    # password = "123456"
    # hasher = Argon2ID()
    # hash = hasher.hash_password(password)
    # print(hash)