from tkinter import *
from PNGReader import PNGReader as PR

class PNG_GUI:
    #Parameters of the window
    HEIGHT = 500
    WIDTH = 950

    reader = None

    #Initialize Tkinter window, another buttons, stuff like that
    def __init__(self, master):
        canvas = Canvas(master, height=self.HEIGHT, width=self.WIDTH)
        canvas.pack()


        displayFrame = Frame(master)
        displayFrame.place(relx=0.5, rely=0.2, relheight=0.8, relwidth=0.5)

        self.textVar = StringVar()
        self.displayLabel=Label(displayFrame, textvariable=self.textVar, bg='white')
        self.displayLabel.pack(side='top', fill='both', expand='true')

        self.textVar.set("Hey!")



        frame = Frame(master)
        frame.place(relx=0, rely=0.2, relheight=0.8, relwidth=0.5)


        #Main buttons - assign functions as lambda to buttons
        self.displayImage = Button(frame, text="Display Image", command=lambda: self.PrintImage())
        self.displayImage.pack(side='top', fill='both', expand='true')



        ecbFrame = Frame(frame)
        ecbFrame.pack(side='top', fill='both', expand='true')

        self.ecbC = Button(ecbFrame, text="Cipher ECB", command=lambda: self.CipherECB())
        self.ecbC.pack(side='left', fill='both', expand='true')

        self.ecbD = Button(ecbFrame, text="Decipher ECB", command=lambda: self.DecipherECB())
        self.ecbD.pack(side='left', fill='both', expand='true')



        cbcFrame = Frame(frame)
        cbcFrame.pack(side='top', fill='both', expand='true')

        self.cbcC = Button(cbcFrame, text="Cipher CBC", command=lambda: self.CipherCBC())
        self.cbcC.pack(side='left', fill='both', expand='true')

        self.cbcD = Button(cbcFrame, text="Decipher CBC", command=lambda: self.DecipherCBC())
        self.cbcD.pack(side='left', fill='both', expand='true')




        pycryptoFrame = Frame(frame)
        pycryptoFrame.pack(side='top', fill='both', expand='true')

        self.pycryptoC = Button(pycryptoFrame, text="Cipher Pycrypto", command=lambda: self.CipherPycrypto())
        self.pycryptoC.pack(side='left', fill='both', expand='true')

        self.pycryptoD = Button(pycryptoFrame, text="Decipher Pycrypto", command=lambda: self.DecipherPycrypto())
        self.pycryptoD.pack(side='left', fill='both', expand='true')




        compressedFrame = Frame(frame)
        compressedFrame.pack(side='top', fill='both', expand='true')

        self.compressedC = Button(compressedFrame, text="Cipher Compressed", command=lambda: self.CipherCompressed())
        self.compressedC.pack(side='left', fill='both', expand='true')

        self.compressedD = Button(compressedFrame, text="Decipher Compressed", command=lambda: self.DecipherCompressed())
        self.compressedD.pack(side='left', fill='both', expand='true')



        self.blank = Button(frame, text="-_________-", command=lambda: self.PrintImage())
        self.blank.pack(side='top', fill='both', expand='true')



        #Collect user input, output to the window
        entryFrame = Frame(master)
        entryFrame.place(relx=0, rely=0, relheight=0.2, relwidth=1)

        self.welcomeLabel = Label(entryFrame, bg='gray', text='Enter PNG Image name below!', font=70)
        self.welcomeLabel.pack(side='top', fill='both', expand='true')

        self.entry = Entry(entryFrame, font=2, bg='yellow')
        self.entry.pack(side='left', fill='x', expand='true')

        self.findImageButton = Button(entryFrame, text="Analyze Image!", command=lambda: self.startProcessing(self.entry.get()))
        self.findImageButton.pack(side='left', fill='x', expand='true')


    #-_______________________________________________________-
    
    def PrintImage(self):
        self.reader.printImg()



    def CipherECB(self):
        self.reader.encryption = 1
        self.reader.whichMethod = 0
        self.reader.readPNG()

    def DecipherECB(self):
        self.reader.encryption = -1
        self.reader.whichMethod = 0
        self.reader.readPNG()




    def CipherCBC(self):
        self.reader.encryption = 1
        self.reader.whichMethod = 1
        self.reader.readPNG()

    def DecipherCBC(self):
        self.reader.encryption = -1
        self.reader.whichMethod = 1
        self.reader.readPNG()




    def CipherPycrypto(self):
        pass

    def DecipherPycrypto(self):
        pass




    def CipherCompressed(self):
        self.reader.encryption = 1
        self.reader.whichMethod = 2
        self.reader.readPNG()

    def DecipherCompressed(self):
        self.reader.encryption = -1
        self.reader.whichMethod = 2
        self.reader.readPNG()




    def startProcessing(self, name):
        self.reader = PR(name) 

#go with it 
root = Tk()
b = PNG_GUI(root)
root.mainloop()
