from tkinter import *
from PNGReader import PNGReader as PR

class PNG_GUI:
    #Parameters of the window
    HEIGHT = 500
    WIDTH = 950

    reader = PR()

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

        self.displayCriticalButton = Button(frame, text="Cipher with self-made algorithm (naive)", command=lambda: self.SelfMadeNaive())
        self.displayCriticalButton.pack(side='top', fill='both', expand='true')

        self.displayAncillaryButton = Button(frame, text="Cipher with self-made algorithm (non-naive)", command=lambda: self.SelfMadeComplicated())
        self.displayAncillaryButton.pack(side='top', fill='both', expand='true')

        self.displayPalette = Button(frame, text="Cipher with algorithm from library", command=lambda: self.LibraryMade())
        self.displayPalette.pack(side='top', fill='both', expand='true')

        self.displayPalette = Button(frame, text="Compare three methods", command=lambda: self.CompareCipher())
        self.displayPalette.pack(side='top', fill='both', expand='true')

        self.fourierButton = Button(frame, text="Decipher", command=lambda: self.Decipher())
        self.fourierButton.pack(side='top', fill='both', expand='true')


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

    def SelfMadeNaive(self):
        pass

    def Decipher(self):
        pass

    def SelfMadeComplicated(self):
        pass

    def LibraryMade(self):
        pass

    def CompareCipher(self):
        pass



    def startProcessing(self, name):
        self.reader.readPNG(name)


#go with it 
root = Tk()
b = PNG_GUI(root)
root.mainloop()
