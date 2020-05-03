import sympy as sy

class NaiveRSA:

    keysize = 8
    realKeyLength = None

    p = None
    q = None
    n = None
    fi = None
    e = None

    pub_key = None
    pri_key = None

    encrBuff = None
    decrBuff = None

    def __init__(self):
        self.p = sy.randprime(2**(self.keysize//2 - 1), 2**(self.keysize//2))
        self.q = sy.randprime(self.p + 1, 2**(self.keysize//2))
        self.n = self.p * self.q

        self.realKeyLength = int.bit_length(self.n)    

        self.fi = (self.p - 1) * (self.q - 1)
        self.e = sy.randprime(2, self.n)

        self.d = sy.mod_inverse(self.e, self.fi)

        if self.n and self.e and self.d == None:
            self.pub_key = (self.e, self.n)
            self.pri_key = (self.d, self.n)


    def Encrypt(self, data):
        self.encrBuff = pow(data, self.e, self.n)
        return self.encrBuff

    def Decrypt(self, data):
        self.decrBuff = pow(data, self.d, self.n)
        return self.decrBuff





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