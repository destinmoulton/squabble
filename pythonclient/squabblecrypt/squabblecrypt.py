from Crypto.Cipher import AES # encryption library

class SquabbleCrypt:
    def __init__(self):
        self.BLOCK_SIZE = 32
        self.PADDING = '{'

    # Pad the text for AES encryption
    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING

    # Create a cipher object using the random secret
    def setPassphrase(self, passphrase):
        self.cipher = AES.new(passphrase)
        
    # Encrypt with AES encode with base64
    def encode(self, s):
        return base64.b64encode(self.cipher.encrypt(self.pad(s)))

    # Decrypt base64 encoded AES encryption
    def decode(self, e):
        return self.cipher.decrypt(base64.b64decode(e)).rstrip(self.PADDING)
