#IHDR
class HeaderChunk:
    #things described in header
    width = None
    height = None
    bitDepth = None
    colorType = None
    compressionMethod = None
    filterMethod = None
    interlaceMethod = None

    multiplier = None
    
    #read according to png documentation + scale width if neccesary (key point in encryption method used)
    def readChunk(self, f, datalen, fwrite, scale):

        wdt = f.read(4)
        self.width = int.from_bytes(wdt, byteorder='big')
        fwrite.write(int(self.width*scale).to_bytes(4, byteorder='big'))

        hgh = f.read(4)
        self.height = int.from_bytes(hgh, byteorder='big')
        fwrite.write(hgh)

        bDp = f.read(1)
        self.bitDepth = int.from_bytes(bDp, byteorder='big') 
        fwrite.write(bDp)

        cTp = f.read(1)
        self.colorType = int.from_bytes(cTp, byteorder='big') 
        fwrite.write(cTp)

        #set multiplier thats used in encryption/decryption

        if self.colorType == 0:
            self.multiplier = 1 * (self.bitDepth // 8)

        elif self.colorType == 2:
            self.multiplier = 3 * (self.bitDepth // 8)

        elif self.colorType == 3:
            self.multiplier = 1 * (self.bitDepth // 8)

        elif self.colorType == 4:
            self.multiplier = 2 * (self.bitDepth // 8)

        elif self.colorType == 6:
            self.multiplier = 4 * (self.bitDepth // 8)

        else:
            self.multiplier = 3 * (self.bitDepth // 8)
        

        cmpMth = f.read(1)
        self.compressionMethod = int.from_bytes(cmpMth, byteorder='big') 
        fwrite.write(cmpMth)

        fltMth = f.read(1)
        self.filterMethod = int.from_bytes(fltMth, byteorder='big') 
        fwrite.write(fltMth)

        intMth = f.read(1)
        self.interlaceMethod = int.from_bytes(intMth, byteorder='big')
        fwrite.write(intMth)
        
        fwrite.write(f.read(4))  

    #what number -> what image type
    def switchColorType(self, num):
        switcher = {
            0: "Grayscale",
            2: "TrueColor",
            3: "Indexed",
            4: "Grayscale + Alpha",
            6: "Truecolor + Alpha",
        }

        return switcher.get(num, "Unknown value.")

    #what number -> interlace
    def switchInterlaceMethod(self, num):
        switcher = {
            0: "No interlace",
            1: "Adam7 interlace",
        }
        return switcher.get(num, "Unknown value.")

    #return it in nice form
    def __str__(self):
        return ("Width: " + str(self.width) + " -----> " + "Width: " + str(self.width) + "px" + "\n"
                "Height: " + str(self.height) + " -----> " + "Height: " + str(self.height) + "px" + "\n"
                "Bit Depth: " + str(self.bitDepth) + " -----> " + "Number of bits per sample: " + str(self.bitDepth) + "\n"
                "Color Type: " + str(self.colorType) + " -----> " + "Color type of the image: " + self.switchColorType(self.colorType) + "\n"
                "Compression Method: " + str(self.compressionMethod) + " -----> " + "Deflate/inflate compression with a 32K sliding window" + "\n"
                "Filter Method: " + str(self.filterMethod) + " -----> " + "Filter method used: " + "Adaptive filtering with five basic filter types" + "\n"
                "Interlace Method: " + str(self.interlaceMethod) + " -----> " + "Interlace method used: " + self.switchInterlaceMethod(self.interlaceMethod) + "\n")

    def clear(self):
        self.width = None
        self.height = None
        self.bitDepth = None
        self.colorType = None
        self.compressionMethod = None
        self.filterMethod = None
        self.interlaceMethod = None        
