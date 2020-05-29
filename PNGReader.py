from enum import IntEnum

from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt

from MyRSA import MyRSA as RSA
from PyCro import PyCro 

from HeaderChunk import HeaderChunk

import zlib

#Assign hex to the most popular chunks header names
class HexTypes(IntEnum):
    #PNG SIGNATURE CONSTANT
    PNG_FILE = 0x89504E470D0A1A0A

    #PNG CHUNK TYPES CONSTANTS (4 CHARACTERS, CODED IN HEX EG. IHDR -> 0x49484452)
    PNG_IHDR = 0x49484452
    PNG_PLTE = 0x504C5445
    PNG_IDAT = 0x49444154
    PNG_IEND = 0x49454E44
    
    PNG_TEXT = 0x74455874
    PNG_EXIF = 0x65584966
    PNG_TRNS = 0x74524E53
    PNG_GAMA = 0x67414D41
    PNG_CHRM = 0x6348524D
    PNG_SRGB = 0x73524742
    PNG_ICCP = 0x69434350
    PNG_ZTXT = 0x7A545874
    PNG_ITXT = 0x69545874
    PNG_BKGD = 0x624B4744
    PNG_PHYS = 0x70485973
    PNG_SBIT = 0x73424954
    PNG_SPLT = 0x73504C54
    PNG_HIST = 0x68495354
    PNG_TIME = 0x74494D45

        
class PNGReader:
    #name of the file
    name = ""

    #Our 2 encryption objects
    enc = None
    pycro = None

    # encryption flag: 1 - encryption, -1 - decrytpion
    encryption = 0

    #variable used in en/decryption of compressed file
    originalIDATWhatsLeft = 0
    
    # name of encrypted, decrypted image
    cipheredName = None
    decipheredName = None

    # variable that holds real key length
    bytesKeyLength = None

    # Method: ECB - 0, CBC - 1, Encrypt compressed - 2, PyCrypto - -1
    whichMethod = 0

    # object connected with header metadata info
    headInfo = HeaderChunk()

    def __init__(self, name):

        #find file in res folder
        self.name = "res/" + name

        self.img = cv2.imread(self.name)

        # results in resluts/ folder
        self.cipheredName = "results/RSA" + name
        self.decipheredName = "results/DEC" + name

        #initialize objects
        self.enc = RSA()
        self.pycro = PyCro()


    #read image - most important function
    def readPNG(self):
        # open read file according do performed operation
        if self.encryption == 1:
            self.f = open(self.name, "rb")
        elif self.encryption == -1:
            self.f  = open(self.cipheredName, "rb")        

        header = self.f.read(8)

        # open file that data will be written to, according to current operation
        if self.encryption == 1:
            fwrite = open(self.cipheredName, "wb+")
        elif self.encryption == -1:
            fwrite = open(self.decipheredName, "wb+")
            
        fwrite.write(header)

        #check if png
        if int.from_bytes(header, byteorder='big') == HexTypes.PNG_FILE:
            #until IEND occurs
            while True:
                byteLen = self.f.read(4)
                #get chunk length
                datalen = int.from_bytes(byteLen, byteorder='big')
                print("Incoming chunk's length: " + str(datalen))
                #get chunk type
                chunkType = self.f.read(4)
                
                if int.from_bytes(chunkType, byteorder='big') != HexTypes.PNG_IDAT:
                    fwrite.write(byteLen)
                    fwrite.write(chunkType)

# Critical Chunks

                #check what chunk, peform appropriate action defined in certain chunk class
                if int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IHDR:
                    print("Incoming chunk's name: IHDR")
                    # multiply width (write to metadata) if the file that we are writing to is encrypted file
                    if self.encryption == 1 and self.whichMethod != 2:
                        self.headInfo.readChunk(self.f, datalen, fwrite, 2)

                    # divide by 2 if we are reading encrypted file and we writing to decrypted.
                    elif self.encryption == -1 and self.whichMethod != 2:
                        self.headInfo.readChunk(self.f, datalen, fwrite, 0.5)
                    
                    # else: do not change metadata
                    else:   
                        self.headInfo.readChunk(self.f, datalen, fwrite, 1)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PLTE:
                    print("Incoming chunk's name: PLTE")
                    self.readTillEnd(datalen, fwrite)
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IDAT:
                    print("Incoming chunk's name: IDAT")

                    # preform appriopriate encryption/decryption according to flags
                    if self.encryption == 1:
                        if self.whichMethod == -1:
                            self.encryptPyCro(datalen, fwrite)
                        elif self.whichMethod != 2:
                            self.encryptDecomp(datalen, fwrite)
                        else:
                            self.EncryptIDAT(datalen, fwrite)

                    elif self.encryption == -1:
                        if self.whichMethod == -1:
                            self.decryptPyCro(datalen, fwrite)
                        if self.whichMethod != 2:
                            self.decryptDecomp(datalen, fwrite)
                        else:
                            self.DecryptIDAT(datalen, fwrite)

                    else:
                        self.readTillEnd(datalen, fwrite)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IEND:
                    print("Incoming chunk's name: IEND")
                    self.readTillEnd(datalen, fwrite)
                    break
                
# Ancillary Chunks

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_EXIF:
                    print("Incoming chunk's name: eXIf")
                    self.readTillEnd(datalen, fwrite)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TEXT:
                    print("Incoming chunk's name: tEXt")
                    self.readTillEnd(datalen, fwrite)  
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TRNS:
                    print("Incoming chunk's name: tRNS")
                    self.readTillEnd(datalen, fwrite)
                
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_GAMA:
                    print("Incoming chunk's name: gAMA")
                    self.readTillEnd(datalen, fwrite)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_CHRM:
                    print("Incoming chunk's name: cHRM")
                    self.readTillEnd(datalen, fwrite)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_SRGB:
                    print("Incoming chunk's name: sRGB")
                    self.readTillEnd(datalen, fwrite)   

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_ICCP:
                    print("Incoming chunk's name: iCCP")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_ZTXT:
                    print("Incoming chunk's name: zTXt")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_ITXT:
                    print("Incoming chunk's name: iTXt")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_BKGD:
                    print("Incoming chunk's name: bkGD")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PHYS:
                    print("Incoming chunk's name: pHYs")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_SBIT:
                    print("Incoming chunk's name: sBIT")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_SPLT:
                    print("Incoming chunk's name: sPLT")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_HIST:
                    print("Incoming chunk's name: hIST")
                    self.readTillEnd(datalen, fwrite)  

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_TIME:
                    print("Incoming chunk's name: tIME")
                    self.readTillEnd(datalen, fwrite)  

                else:
                    self.readTillEnd(datalen, fwrite)

                print()
        else:
            print("That's not even a PNG file!")
        self.f.close()


    #read all whats left to go to next chunk
    def readTillEnd(self, datalen, fwrite):
        for _ in range(datalen+4):
            tmp = self.f.read(1)
            fwrite.write(tmp)

#***********************************************************************************************************************************#
#***********************************************************************************************************************************#
#***********************************************************************************************************************************#

    ########################################################################
    # ENCRYPT COMPRESSED IDAT                                              #
    ########################################################################
    def EncryptIDAT(self, datalen, fwrite):
        # variable used in counting read bytes of IDAT
        readBytes = 0
        # flag that signalizes whether we can divide IDAT into desired pieces, without problems
        isNotGood = 0

        # variable that helps to adjust IDAT new size
        howManyBytes = 0

        # get byte lenght of key
        bytesKeyLength = (self.enc.realKeyLength + 7) // 8

        # check if division of the file will be nice - tell how many times the loop will go
        if datalen % bytesKeyLength // 2 == 0:
            howMany = 2*(datalen // bytesKeyLength)
        else:
            howMany = 2*(datalen // bytesKeyLength) + 1 
            isNotGood = 1

        # Encrypted bytes list
        thaBytes = []


        # main action - get byte series, with length = bytesKeyLength //2, convert to int, encrypt, put into list 
        for i in range(howMany):
            # if i = howMany - 1 and we cannot divide without problems, adjust read bytes
            if isNotGood == 1 and i == howMany - 1: 
                tmp = self.f.read(datalen - readBytes)
                self.IDATwhatsLeft = datalen - readBytes
                zz = self.enc.EncryptECB(int.from_bytes(tmp, byteorder='big'))
                thaBytes.append(zz)
                readBytes += datalen - readBytes
            else:
                tmp = self.f.read(bytesKeyLength // 2)
                zz = self.enc.EncryptECB(int.from_bytes(tmp, byteorder='big'))
                thaBytes.append(zz)
                readBytes += bytesKeyLength // 2

            howManyBytes += bytesKeyLength

        # write new IDAT length and name
        fwrite.write(howManyBytes.to_bytes(4, byteorder='big'))
        fwrite.write(HexTypes.PNG_IDAT.to_bytes(4, byteorder='big'))

        # write encrypted bytes, after converting back to bytes
        for i in thaBytes:
            fwrite.write(i.to_bytes(bytesKeyLength, byteorder='big'))


        # crc
        fwrite.write(self.f.read(4))

    ########################################################################
    # DECRYPT COMPRESSED IDAT                                              #
    ########################################################################
    def DecryptIDAT(self, datalen, fwrite):
        # length of key in bytes
        bytesKeyLength = (self.enc.realKeyLength + 7) // 8

        # how many times loop goes
        howMany = (datalen // bytesKeyLength)


        # write to decrypted files, length of IDAT
        fwrite.write((bytesKeyLength//2 * (howMany - 1) + self.IDATwhatsLeft).to_bytes(4, byteorder='big'))
        fwrite.write(HexTypes.PNG_IDAT.to_bytes(4, byteorder='big'))
        

        # go throught idat, decrypt bytes series, and write them to file
        for i in range(howMany):
            tmp = self.f.read(bytesKeyLength)
            zz = self.enc.DecryptECB(int.from_bytes(tmp, byteorder='big'))
            if i == howMany - 1: 
                fwrite.write(zz.to_bytes(self.IDATwhatsLeft , byteorder='big'))
            else:
                fwrite.write(zz.to_bytes(bytesKeyLength // 2, byteorder='big'))

        fwrite.write(self.f.read(4))
      
#***********************************************************************************************************************************#
#***********************************************************************************************************************************#
#***********************************************************************************************************************************#

    ########################################################################
    # ENCRYPT DECOMPRESSED IDAT                                            #
    ########################################################################
    def encryptDecomp(self, datalen, fwrite):
        # read compressed bytes
        thaBytes = []
        for _ in range(datalen):
            thaBytes.append(self.f.read(1))
        
        # decompress em
        IDAT_Decomp = zlib.decompress(b''.join(thaBytes))

        # organize bytes in matrix = hegiht x width(times multiplier = color type)
        nicerIDAT = np.zeros((self.headInfo.height, self.headInfo.width*self.headInfo.multiplier+1), dtype=int)

        for i in range(self.headInfo.height):
            for j in range(self.headInfo.width*self.headInfo.multiplier+1):
                nicerIDAT[i][j] = IDAT_Decomp[i*(self.headInfo.width*self.headInfo.multiplier+1) + j]

        niceIDAT = nicerIDAT.tolist()
        

        # byte size of the key
        bytesKeyLength = (self.enc.realKeyLength + 7) // 8
        isWrong = 0

        # adjust loop size, to the condition wheter we can divide image into nice pieces or not
        if (self.headInfo.width*self.headInfo.multiplier) % (bytesKeyLength//2) == 0:
            wieViel = 2*(self.headInfo.width*self.headInfo.multiplier) // bytesKeyLength
        else:
            isWrong = 1
            wieViel = 2*(self.headInfo.width*self.headInfo.multiplier) // bytesKeyLength  + 1

        ciphIDAT = []

        # add filter number, analize particular row
        for j in range(self.headInfo.height):
            ciphIDAT.append(int(niceIDAT[j][0]).to_bytes(1, byteorder='big'))
            for i in range(wieViel):
                # according to given method decrypt byte series converted to int
                if self.whichMethod == 0:
                    if isWrong == 1 and i == wieViel - 1:
                        zz = self.enc.EncryptECB(int.from_bytes(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength // 2)) : ((self.headInfo.width*self.headInfo.multiplier) + 1)]), byteorder='big')) 
                    else:
                        zz = self.enc.EncryptECB(int.from_bytes(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength // 2)) : ((i+1)*bytesKeyLength // 2 + 1)]), byteorder='big')) 
              
                elif self.whichMethod == 1:
                    if isWrong == 1 and i == wieViel - 1:
                        zz = self.enc.EncryptCBC(int.from_bytes(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength // 2)) : ((self.headInfo.width*self.headInfo.multiplier) + 1)]), byteorder='big'), i) 
                    else:
                        zz = self.enc.EncryptCBC(int.from_bytes(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength // 2)) : ((i+1)*bytesKeyLength // 2 + 1)]), byteorder='big'), i)    

                else:
                    print("Unknown method!")
                
                # put resutls in the list
                ciphIDAT.append(zz.to_bytes(bytesKeyLength, byteorder='big'))

        # join list and compress it
        w = b''.join(ciphIDAT)
        ccc = zlib.compress(w)

        # write everythang to encrypted file
        fwrite.write(len(ccc).to_bytes(4, byteorder='big'))
        fwrite.write(HexTypes.PNG_IDAT.to_bytes(4, byteorder='big'))
        fwrite.write(ccc)
        fwrite.write(self.f.read(4))



    ########################################################################
    # DECRYPT DECOMPRESSED IDAT                                            #
    ########################################################################
    def decryptDecomp(self, datalen, fwrite):
        # read bytes and decompress em
        thaBytes = []
        for _ in range(datalen):
            thaBytes.append(self.f.read(1))
        
        IDAT_Decomp = zlib.decompress(b''.join(thaBytes))


        # organize bytes into nice matric
        nicerIDAT = np.zeros((self.headInfo.height, self.headInfo.width*self.headInfo.multiplier +1), dtype=int)

        for i in range(self.headInfo.height):
            for j in range(self.headInfo.width*self.headInfo.multiplier+1):
                nicerIDAT[i][j] = IDAT_Decomp[i*(self.headInfo.width*self.headInfo.multiplier+1) + j]

        niceIDAT = nicerIDAT.tolist()

        # get key length in bytes, set loop size
        bytesKeyLength = (self.enc.realKeyLength + 7) // 8

        wieViel = (self.headInfo.width*self.headInfo.multiplier) // bytesKeyLength 

        ciphIDAT = []

        # put filter type, according to method decrypt bytes
        for j in range(self.headInfo.height):
            ciphIDAT.append(int(niceIDAT[j][0]).to_bytes(1, byteorder='big'))
            for i in range(wieViel):

                if self.whichMethod == 0:
                    zz = self.enc.DecryptECB(int.from_bytes(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength)) : ((i+1)*bytesKeyLength + 1)]), byteorder='big')) 

                elif self.whichMethod == 1:
                    zz = self.enc.DecryptCBC(int.from_bytes(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength)) : ((i+1)*bytesKeyLength + 1)]), byteorder='big'), i)  

                else:
                    print("Unknown method!")
                
                # put everyting to the list
                ciphIDAT.append(zz.to_bytes(bytesKeyLength // 2, byteorder='big'))



        # join and compress
        w = b''.join(ciphIDAT)
        ccc = zlib.compress(w)
        
        # write everyting
        fwrite.write(len(ccc).to_bytes(4, byteorder='big'))
        fwrite.write(HexTypes.PNG_IDAT.to_bytes(4, byteorder='big'))
        fwrite.write(ccc)
        fwrite.write(self.f.read(4))

#***********************************************************************************************************************************#
#***********************************************************************************************************************************#
#***********************************************************************************************************************************#

    ########################################################################
    # ENCRYPT USING LIBRARY                                                #
    ########################################################################
    def encryptPyCro(self, datalen, fwrite):
        # like always decompress everyting, orginize into nice matrix, get keylenght in bytes
        thaBytes = []
        for _ in range(datalen):
            thaBytes.append(self.f.read(1))
        
        IDAT_Decomp = zlib.decompress(b''.join(thaBytes))

        nicerIDAT = np.zeros((self.headInfo.height, self.headInfo.width*self.headInfo.multiplier+1), dtype=int)

        for i in range(self.headInfo.height):
            for j in range(self.headInfo.width*self.headInfo.multiplier+1):
                nicerIDAT[i][j] = IDAT_Decomp[i*(self.headInfo.width*self.headInfo.multiplier+1) + j]

        niceIDAT = nicerIDAT.tolist()


        bytesKeyLength = PyCro.keyLength  // 8
        isWrong = 0


        # check if we can divide it nicely, (we divide into blocks keysize / 2)
        if (self.headInfo.width*self.headInfo.multiplier) % (bytesKeyLength//2) == 0:
            wieViel = 2*(self.headInfo.width*self.headInfo.multiplier) // bytesKeyLength
        else:
            isWrong = 1
            wieViel = 2*(self.headInfo.width*self.headInfo.multiplier) // bytesKeyLength + 1

        ciphIDAT = []

        # put filter type, analize row, encrypt with library encryptions
        for j in range(self.headInfo.height):
            ciphIDAT.append(int(niceIDAT[j][0]).to_bytes(1, byteorder='big'))
            for i in range(wieViel):
                if isWrong == 1 and i == wieViel - 1:
                    zz = self.pycro.encrypt(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength // 2)) : ((self.headInfo.width*self.headInfo.multiplier) + 1)])) 
                else:
                     zz = self.pycro.encrypt(bytearray(niceIDAT[j][(1 + (i * bytesKeyLength // 2)) : ((i+1)*bytesKeyLength // 2 + 1)]))    
                
                # put everyting to lthe ist
                ciphIDAT.append(int.from_bytes(zz, byteorder='big').to_bytes(bytesKeyLength, byteorder='big'))

        # join and compress it
        w = b''.join(ciphIDAT)
        ccc = zlib.compress(w)

        # write everything to file
        fwrite.write(len(ccc).to_bytes(4, byteorder='big'))
        fwrite.write(HexTypes.PNG_IDAT.to_bytes(4, byteorder='big'))
        fwrite.write(ccc)
        fwrite.write(self.f.read(4))




    #Weird Errors, hard to verify (outer library used)
    def decryptPyCro(self, datalen, fwrite):
        pass




    #print it with cv2
    def printImg(self):
        cv2.imshow('Analyzed Image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
