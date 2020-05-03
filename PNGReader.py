from enum import IntEnum

from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt

from NaiveRSA import NaiveRSA as NR

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

    enc = None

    #read image - most important function
    def readPNG(self, name):
        # assign name of the file, file handler, as well read this with cv2
        self.name = name
        self.f = open(self.name, "rb")
        self.img = cv2.imread(self.name)

        self.enc = NR()
        
        header = self.f.read(8)

        fwrite = open("RSA" + self.name, "wb+")
        fwrite.write(header)

        #check if png
        if int.from_bytes(header, byteorder='big') == HexTypes.PNG_FILE:
            #until IEND occurs
            while True:

                byteLen = self.f.read(4)
                fwrite.write(byteLen)
                #get chunk length
                datalen = int.from_bytes(byteLen, byteorder='big')
                print("Incoming chunk's length: " + str(datalen))
                #get chunk type
                chunkType = self.f.read(4)
                fwrite.write(chunkType)

# Critical Chunks

                #check what chunk, peform appropriate action defined in certain chunk class
                if int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IHDR:
                    print("Incoming chunk's name: IHDR")
                    self.readTillEnd(datalen, fwrite)

                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_PLTE:
                    print("Incoming chunk's name: PLTE")
                    self.readTillEnd(datalen, fwrite)
                    
                elif int.from_bytes(chunkType, byteorder='big') == HexTypes.PNG_IDAT:
                    print("Incoming chunk's name: IDAT")
                    self.EncryptIDAT(datalen, fwrite)

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

    
    def EncryptIDAT(self, datalen, fwrite):

        readBytes = 0

        bytesKeyLength = self.enc.realKeyLength / 8
        if isinstance(bytesKeyLength, float):
            bytesKeyLength = int(bytesKeyLength)

        for _ in range(datalen):
            if bytesKeyLength <= datalen - readBytes:
                tmp = self.f.read(bytesKeyLength)
                fwrite.write(self.enc.Encrypt(int.from_bytes(tmp, byteorder='big')).to_bytes(bytesKeyLength, byteorder='big'))
                readBytes += bytesKeyLength
            else:
                if readBytes == 0:
                    print(datalen - readBytes)
                tmp = self.f.read(datalen - readBytes)
                fwrite.write(self.enc.Encrypt(int.from_bytes(tmp, byteorder='big')).to_bytes(datalen - readBytes, byteorder='big'))
                readBytes += (datalen - readBytes)

        fwrite.write(self.f.read(4))


    #print it with cv2
    def printImg(self):
        cv2.imshow('Analyzed Image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()