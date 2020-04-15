import hashlib #for sha256 encoding
from PIL import ImageFont, ImageDraw #for fonts
from tkinter import *
import tkinter.font
import string
import os

'''
TODO LIST:
- minor refinement changes in comments throughout code marked "TODO"
- home page
- instructions page
- upload page
- profile page
- progress page
- practice page

NOTES:
- profile.txt is of the format: 
    num_decks\n
    deck_name:mastery
    deck_name:mastery
    ...
'''


################################################################################
# initializer
################################################################################

def init(data):
    data.mode = "start"
    data.loginButton = Button(data.width/2, data.height*0.55, 100, 30, "Login")
    data.registerButton = Button(data.width/2, data.height*0.7, 100, 30, "Register")
    data.creditButton = Button(data.width*0.9, data.height*0.9, 70, 25, "Credit")
    data.creditBackButton = Button(data.width/2, data.height*0.85, 80, 25, "< Back")
    data.submitButton = Button(data.width/2, data.height*0.8, 80, 25, "Submit")
    data.underlineBackButton = UnderlineButton(data.width/2, data.height*0.9,
        30, 20, "Back")
    data.password = ""
    data.username = ""
    data.inputPassword = False
    data.inputUsername = False
    data.warnings = ""
    data.profileButton = Button(data.width*0.9, data.height*0.08, 65, 25, "Profile")
    data.practiceAllButton = Button(data.width/2, data.height*0.9, 100, 25, "Practice All")
    data.logoutButton = UnderlineButton(data.width*0.08, data.height*0.08, 35, 15, "Logout")

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
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, 
        x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, 
        y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
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

    def onPress(self, x, y):
        if (self.x0 < x < self.x1) and (self.y0 < y < self.y1):
            return True

class UnderlineButton(Button):
    def draw(self, canvas, fontSize):
        canvas.create_line(self.x0, self.y1, self.x1, self.y1, width=2, 
            fill="black")
        canvas.create_text(self.x, self.y, text=self.text, font=getFont(fontSize))

def drawDeck(canvas, data, row, deck, deckName, fillColor="white"):
    #print(deckName, row)
    for i in range(4, 0, -1):
        x0 = data.width*0.12 + data.width*0.2*deck + i*3
        y0 = data.height*0.2 + data.height*0.2*row + i*3
        x1 = x0 + data.width*0.15
        y1 = y0 + data.height*0.15
        roundRectangle(canvas, x0, y0, x1, y1, fill=fillColor, width=2, outline="black")
    canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text=deckName, font=getFont(25)) 

################################################################################
# start mode
################################################################################

def startMousePressed(event, data):
    if data.loginButton.onPress(event.x, event.y):
        data.mode = "login"
    elif data.registerButton.onPress(event.x, event.y):
        data.mode = "register"
    elif data.creditButton.onPress(event.x, event.y):
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
    if data.creditBackButton.onPress(event.x, event.y):
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
# register mode
################################################################################

def registerMousePressed(event, data):
    if (data.width*0.42 < event.x < data.width*0.7) and (data.height*0.35 < event.y < data.height*0.45):
        data.inputUsername = True
    else:
        data.inputUsername = False
    if (data.width*0.42 < event.x < data.width*0.7) and (data.height*0.49 < event.y < data.height*0.59):
        data.inputPassword = True
    else:
        data.inputPassword = False

    if data.submitButton.onPress(event.x, event.y):
        #TODO: store all this on mongodb instead of local files 
        if os.path.isdir("users/%s" % data.username):
            #if an existing user, can't create this 
            data.warnings = "Username already in use. Please select a different one."
        else:
            os.mkdir("users/%s" % data.username)
            #f = open("users/%s/credentials.txt" % data.username,"w+")
            hashedPass = hashlib.sha256(data.password.encode('utf-8')).hexdigest()
            #f.write(hashedPass)
            writeFile("users/%s/credentials.txt" % data.username, hashedPass)
            writeFile("users/%s/profile.txt" % data.username, "0")
            data.password = ""
            data.username = ""
            data.warnings = ""
            data.user = data.username
            data.mode = "home"
    if data.underlineBackButton.onPress(event.x, event.y):
        data.mode = "start"
        data.password = ""
        data.username = ""
        data.warnings = ""

def registerKeyPressed(event, data):
    if data.inputUsername:
        if event.keysym == "BackSpace":
            if len(data.username) > 0:
                data.username = data.username[:-1]
        elif event.keysym == "Tab":
            data.inputUsername = False
            data.inputPassword = True
        elif len(event.keysym) == 1:
            data.username += event.keysym
    elif data.inputPassword:
        if event.keysym == "BackSpace":
            if len(data.password) > 0:
                data.password = data.password[:-1]
        elif len(event.keysym) == 1:
            data.password += event.keysym


def registerTimerFired(data):
    pass

def registerRedrawAll(canvas, data):
    drawIndexCard(canvas, data)
    canvas.create_text(data.width/2, data.height*0.1, text="Register as new user",
        font=getFont(35))
    data.submitButton.draw(canvas, 25)
    data.underlineBackButton.draw(canvas, 20)
    canvas.create_text(data.width*0.3, data.height*0.4, text="username:",
        font=getFont(30))
    canvas.create_text(data.width*0.3, data.height*0.54, text="password:",
        font=getFont(30))
    userOutline = "#12e3ff" if data.inputUsername else "black" #TODO: change color
    passOutline = "#12e3ff" if data.inputPassword else "black"
    roundRectangle(canvas, data.width*0.42, data.height*0.35, data.width*0.7,
        data.height*0.45, width=2, outline=userOutline, fill="white")
    roundRectangle(canvas, data.width*0.42, data.height*0.49, data.width*0.7,
        data.height*0.59, width=2, outline=passOutline, fill="white")
    canvas.create_text(data.width*0.44, data.height*0.4, text=data.username,
        font=getFont(25), anchor=W) #TODO: overflow of printing if string too long
    canvas.create_text(data.width*0.44, data.height*0.54, text="*"*len(data.password),
        font=getFont(25), anchor=W)
    canvas.create_text(data.width*0.1, data.height*0.26, text=data.warnings,
        font=getFont(25), anchor=W, fill="#ff4747")

################################################################################
# login mode
################################################################################

def loginMousePressed(event, data):
    if (data.width*0.42 < event.x < data.width*0.7) and (data.height*0.35 < event.y < data.height*0.45):
        data.inputUsername = True
    else:
        data.inputUsername = False
    if (data.width*0.42 < event.x < data.width*0.7) and (data.height*0.49 < event.y < data.height*0.59):
        data.inputPassword = True
    else:
        data.inputPassword = False

    if data.submitButton.onPress(event.x, event.y):
        hashedPass = hashlib.sha256(data.password.encode('utf-8')).hexdigest()
        if not os.path.isdir("users/%s" % data.username):
            data.warnings = "This user does not exist. Please try again."
        elif hashedPass != readFile("users/%s/credentials.txt" % data.username):
            data.warnings = "Your password is incorrect. Please try again."
        else:
            data.user = data.username
            data.mode = "home"
            data.password = ""
            data.username = ""
            data.warnings = ""

    if data.underlineBackButton.onPress(event.x, event.y):
        data.mode = "start"
        data.password = ""
        data.username = ""
        data.warnings = ""


def loginKeyPressed(event, data):
    if data.inputUsername:
        if event.keysym == "BackSpace":
            if len(data.username) > 0:
                data.username = data.username[:-1]
        elif event.keysym == "Tab":
            data.inputUsername = False
            data.inputPassword = True
        elif len(event.keysym) == 1:
            data.username += event.keysym
    elif data.inputPassword:
        if event.keysym == "BackSpace":
            if len(data.password) > 0:
                data.password = data.password[:-1]
        elif len(event.keysym) == 1:
            data.password += event.keysym

def loginTimerFired(data):
    pass

def loginRedrawAll(canvas, data):
    drawIndexCard(canvas, data)
    canvas.create_text(data.width/2, data.height*0.1, text="Login as existing user",
        font=getFont(35))
    data.submitButton.draw(canvas, 25)
    data.underlineBackButton.draw(canvas, 20)
    canvas.create_text(data.width*0.3, data.height*0.4, text="username:",
        font=getFont(30))
    canvas.create_text(data.width*0.3, data.height*0.54, text="password:",
        font=getFont(30))
    userOutline = "#12e3ff" if data.inputUsername else "black" #TODO: change color to be more aesthetic
    passOutline = "#12e3ff" if data.inputPassword else "black"
    roundRectangle(canvas, data.width*0.42, data.height*0.35, data.width*0.7,
        data.height*0.45, width=2, outline=userOutline, fill="white")
    roundRectangle(canvas, data.width*0.42, data.height*0.49, data.width*0.7,
        data.height*0.59, width=2, outline=passOutline, fill="white")
    canvas.create_text(data.width*0.44, data.height*0.4, text=data.username,
        font=getFont(25), anchor=W) #TODO: overflow of printing if string too long
    canvas.create_text(data.width*0.44, data.height*0.54, text="*"*len(data.password),
        font=getFont(25), anchor=W)
    canvas.create_text(data.width*0.2, data.height*0.26, text=data.warnings,
        font=getFont(25), anchor=W, fill="#ff4747")

################################################################################
# home mode
################################################################################

def homeMousePressed(event, data):
    if data.profileButton.onPress(event.x, event.y):
        data.mode = "profile"
    elif data.logoutButton.onPress(event.x, event.y):
        data.mode = "start"
        data.user = ""

def homeKeyPressed(event, data):
    pass

def homeTimerFired(data):
    pass

def homeRedrawAll(canvas, data):
    #TODO: enable scrolling if too many decks on one page 
    drawIndexCard(canvas, data)
    canvas.create_text(data.width/2, data.height*0.1, text="Your Decks",
        font=getFont(40))
    data.profileButton.draw(canvas, 25)
    numDecks = int(readFile("users/%s/profile.txt" % data.user).splitlines()[0])
    decks = readFile("users/%s/profile.txt" % data.user).splitlines()[1:]
    decks = list(map(lambda s: s.split(":")[0], decks))
    for row in range(numDecks//4 + 1):
        for deck in range(4 if (row + 1)*4 <= numDecks else (numDecks % 4)):
            deckName = decks[row*4 + deck]            
            drawDeck(canvas, data, row, deck, deckName)
    uploadRow = (numDecks + 1)//4
    uploadCol = (numDecks + 1) % 4 - 1
    drawDeck(canvas, data, uploadRow, uploadCol, "+Upload", "#d9f5ff")
    data.practiceAllButton.draw(canvas, 25)
    data.logoutButton.draw(canvas, 18)

################################################################################
# mode toggle
################################################################################

def mousePressed(event, data):
    if data.mode == "start":
        startMousePressed(event, data)
    elif data.mode == "credit":
        creditMousePressed(event, data)
    elif data.mode == "register":
        registerMousePressed(event, data)
    elif data.mode == "login":
        loginMousePressed(event, data)
    elif data.mode == "home":
        homeMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "start":
        startKeyPressed(event, data)
    elif data.mode == "credit":
        creditKeyPressed(event, data)
    elif data.mode == "register":
        registerKeyPressed(event, data)
    elif data.mode == "login":
        loginKeyPressed(event, data)
    elif data.mode == "home":
        homeKeyPressed(event, data)

def timerFired(data):
    if data.mode == "start":
        startTimerFired(data)
    elif data.mode == "credit":
        creditTimerFired(data)
    elif data.mode == "register":
        registerTimerFired(data)
    elif data.mode == "login":
        loginTimerFired(data)
    elif data.mode == "home":
        homeTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "start":
        startRedrawAll(canvas, data)
    elif data.mode == "credit":
        creditRedrawAll(canvas, data)
    elif data.mode == "register":
        registerRedrawAll(canvas, data)
    elif data.mode == "login":
        loginRedrawAll(canvas, data)
    elif data.mode == "home":
        homeRedrawAll(canvas, data)


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