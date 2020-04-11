import hashlib #for sha256 encoding
from PIL import ImageFont, ImageDraw #for fonts
from tkinter import *
import tkinter.font
import string

################################################################################
# initializer
################################################################################

def init(data):
    data.mode = "start"
    data.loginButton = Button(data.width/2, data.height*0.55, 100, 30, "Login")
    data.registerButton = Button(data.width/2, data.height*0.7, 100, 30, "Register")
    data.creditButton = Button(data.width*0.9, data.height*0.9, 70, 25, "Credit")
    data.creditBackButton = Button(data.width/2, data.height*0.85, 80, 25, "< Back")

################################################################################
# general helpers/classes
################################################################################

#draws index card pattern on entire canvas
def drawIndexCard(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height)
    canvas.create_line(0, data.height*0.15, data.width, data.height*0.15, 
        fill="#ff7575", width=2) #red
    blueLines = (data.height*0.85)//(data.height*0.07)
    for i in range(int(blueLines)):
        lineY = data.height*0.15 + (i + 1)*data.height*0.07
        canvas.create_line(0, lineY, data.width, lineY, fill="#96eaff", width=2)

def getFont(fontSize):
    #Ink Free
    myFont = tkinter.font.Font(family="Ink Free", size=fontSize, weight="bold")
    return myFont

def roundRectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

#exit canvas
def quit():
    global root
    root.destroy()

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

class Button(object):
    def __init__(self, x, y, w, h, text):
        self.x0 = x - w
        self.x1 = x + w
        self.y0 = y - h
        self.y1 = y + h
        self.x = x
        self.y = y
        self.text = text

    def draw(self, canvas, fontSize):
        roundRectangle(canvas, self.x0, self.y0, self.x1, self.y1, fill='white', 
            width=2, outline="black")
        canvas.create_text(self.x, self.y, text=self.text, font=getFont(fontSize))

    def onPress(self, data, x, y):
        if (self.x0 < x < self.x1) and (self.y0 < y < self.y1):
            return True


################################################################################
# start mode
################################################################################

def startMousePressed(event, data):
    if data.loginButton.onPress(data, event.x, event.y):
        data.mode = "login"
    elif data.registerButton.onPress(data, event.x, event.y):
        data.mode = "register"
    elif data.creditButton.onPress(data, event.x, event.y):
        data.mode = "credit"

def startKeyPressed(event, data):
    pass

def startTimerFired(data):
    pass

def startRedrawAll(canvas, data):
    drawIndexCard(canvas, data)
    canvas.create_text(data.width/2, data.height/3.5, text="Flashcard Tutor",
        font=getFont(60))
    data.loginButton.draw(canvas, 25)
    data.registerButton.draw(canvas, 25)
    data.creditButton.draw(canvas, 25)

################################################################################
# credit mode
################################################################################

def creditMousePressed(event, data):
    if data.creditBackButton.onPress(data, event.x, event.y):
        data.mode = "start"

def creditKeyPressed(event, data):
    pass

def creditTimerFired(data):
    pass

def creditRedrawAll(canvas, data):
    drawIndexCard(canvas, data)
    canvas.create_text(data.width/2, data.height/10, 
        text="This project was made possible by:", font=getFont(25))
    data.creditBackButton.draw(canvas, 25)
    canvas.create_text(data.width*0.1, data.height*0.228, 
        text='''Jenny Yu - CMU class of 2021, ECE major and HCI
        minor. She enjoys digital art, computer science,
        and animals.''',
        font=getFont(25), anchor=NW)
    canvas.create_text(data.width*0.1, data.height*0.5, 
        text='''Ruitao Li - CMU class of 2023, Information Systems
        major. He enjoys video games in his leisure like 
        League of Legends and Plants vs. Zombies.''',
        font=getFont(25), anchor=NW)

################################################################################
# mode toggle
################################################################################

def mousePressed(event, data):
    if data.mode == "start":
        startMousePressed(event, data)
    elif data.mode == "credit":
        creditMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "start":
        startKeyPressed(event, data)
    elif data.mode == "credit":
        creditKeyPressed(event, data)

def timerFired(data):
    if data.mode == "start":
        startTimerFired(data)
    elif data.mode == "credit":
        creditTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "start":
        startRedrawAll(canvas, data)
    elif data.mode == "credit":
        creditRedrawAll(canvas, data)


################################################################################
# main run function
################################################################################

root=Tk()

def run(width=1000, height=550):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    init(data)
    # create the root and the canvas
    #root = Toplevel()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()