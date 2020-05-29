from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from base64 import b64decode,b64encode

class PyCro:

    key = None
    private = None
    public = None
    cipher = None

    keyLength = 1024

    def __init__(self):
        self.key = RSA.generate(self.keyLength, Random.new().read)
        self.private, self.public = self.key, self.key.publickey()
        self.cipher = PKCS1_OAEP.new(self.key)      

    def encrypt(self, msg):
        return self.cipher.encrypt(msg)

    def decrypt(self, msg):
        return self.cipher.decrypt(msg)

#cr = PyCro()
#normal = 132512512352523582358239523958239853298589258923592389523985239582391820571234785346953427895230495
#maszyna = cr.cipher.encrypt(normal.to_bytes(64, byteorder='big'))
#
#print(maszyna)
#print(int.from_bytes(cr.cipher.decrypt(maszyna), byteorder='big'))