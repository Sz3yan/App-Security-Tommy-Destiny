from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

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


if __name__ == "__main__":
    s = Secure()
    print(f"key: {s.get_key()}")
    print(f"iv: {s.get_iv()}")
    print("message: Hello World! ... encrypted message:", s.encrypt(b"Hello World!"))
    print("dencrypted message:",s.decrypt(s.encrypt(b"Hello World!")))