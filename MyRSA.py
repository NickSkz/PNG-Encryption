import sympy as sy
import random

class MyRSA:

    #Set keysize
    keysize = 1024
    realKeyLength = None

    # 2 large primary nr
    p = None
    q = None

    # n = pq
    n = None

    # Funkcja Eulera
    fi = None

    # e, d - key points in en/decryption
    e = None
    d = None
    # Init vector in CBC
    IV = None

    # public and private key
    pub_key = None
    pri_key = None

    # buffers that hold info
    encrBuff = None
    decrBuff = None
    dataBuff = None

    def __init__(self):

        #p, q - random primes in given interval, so thet multiplication gives desired key length
        self.p = sy.randprime(2**(self.keysize//2 - 1), 2**(self.keysize//2))
        self.q = sy.randprime(self.p + 1, 2**(self.keysize//2))
        self.n = self.p * self.q

        # key length - to confirmation
        self.realKeyLength = int.bit_length(self.n)    

        # eurler fun - then pick prime e from the interval
        self.fi = (self.p - 1) * (self.q - 1)
        self.e = sy.randprime(2, self.n)

        # get d, used to decryption
        self.d = sy.mod_inverse(self.e, self.fi)

        # set public and private key
        if self.n and self.e and self.d == None:
            self.pub_key = (self.e, self.n)
            self.pri_key = (self.d, self.n)



        #----------------CBC-----------------
        self.IV = random.getrandbits(self.realKeyLength // 2)


    # encrypt, decrypt ECB according to RSA (modulo exponentation)
    def EncryptECB(self, data):
        self.encrBuff = pow(data, self.e, self.n)
        self.dataBuff = data
        return self.encrBuff

    def DecryptECB(self, data):
        self.dataBuff = data
        self.decrBuff = pow(data, self.d, self.n)
        return self.decrBuff



    #encrypt, decrypt CBC, xor with previous result,  IV - init vector 
    def EncryptCBC(self, data, howMany):
        xored = None
        self.dataBuff = data

        if howMany == 0:
            xored = data ^ self.IV
        else:
            xored = data ^ self.encrBuff

        self.encrBuff = pow(xored, self.e, self.n)
        return self.encrBuff


    def DecryptCBC(self, data, howMany):
        xored = None
        decrypted = pow(data, self.d, self.n)

        if howMany == 0:
            xored = decrypted ^ self.IV
        else:
            xored = decrypted ^ self.dataBuff

        self.dataBuff = data

        return xored



#enc = MyRSA()
#
#encr = enc.EncryptCBC(522, 0)
#encr2 = enc.EncryptCBC(1224, 9)
#
#print(encr)
#print(encr2)
#
#print(enc.DecryptCBC(encr, 0))
#print(enc.DecryptCBC(encr2, 9))






#nRSA = NaiveRSA()

#print("p: " + str(nRSA.p) + "\nq: " + str(nRSA.q) + "\nn: " + str(nRSA.n) + "\ne: " + str(nRSA.e) + "\nd: " + str(nRSA.d)) 
#print("Key size: " + str(int.bit_length(nRSA.n)))

#Test encryption

#orig = 144
#print("Original data: " + str(orig))
#var = nRSA.Encrypt(orig)
#print("Encrypted: " + str(var))
#print("Decrypted: " + str(nRSA.Decrypt(var)))
###