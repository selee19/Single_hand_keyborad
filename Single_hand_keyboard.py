"""
Monash university
FIT 3036 Final year project

Project: One-handed keyboard = S-Keyboard
Project time: 09/03/18 ~ 25/05/18

Student: Seoneui Lee (27136868)
Supervisor: Dr.Rasika Amarasiri

Last modified: 21/05/18
"""

import pygame
from pygame.locals import *


margins = 9,7 #x and y margins between keys

# Main keyboard layout = Char tab
keyboard2 = [
    ['CAP', 'Char', 'Pun', 'Num', 'Short','','delete'],
    ['C', ('I', 'Y'), ('O', 'W'), ('T', 'K'), ('U', 'V'),('.',','),'?'],
    [('D', 'Q'), ('E', 'G'), ('A', 'B'), ('R', 'F'), ('P', 'J'), 'enter'],
    ['M', 'H', 'N', ('S', 'X'), ('L', 'Z'), None],
    ['space', '<', '^', 'v', '>']
    ]

keyboard = [
    ['CAP', 'Char', 'Pun', 'Num', 'Short','','delete'],
    ['U','O',('N', 'V'), ('T', 'Y'), ('H', 'W'), ('.',','),'?'],
    [('I', 'Q'), ('A', 'G'), ('E', 'B'), ('R', 'F'), ('C', 'J'), 'enter'],
    ['M', 'D',('P', 'K'), ('S', 'X'), ('L', 'Z'), None],
    ['space', '<', '^', 'v', '>']
    ]

# Pun tab
punctuation = [
    ['CAP', 'Char', 'Pun', 'Num', 'Short','','delete'],
    [('[', ']'),('(', '{') ,(')', '}'),  '^', '#','$','%',('|', '\\')],
    [(':', ';'), '~', '@', '&','!', 'enter'],
    [("'",'"'), '-', '=', '+', '*', '/'],
    ['space', '<', '^', 'v', '>']
    ]

# Num tab
numbers = [
    ['CAP', 'Char', 'Pun', 'Num', 'Short','','delete'],
    ['1', '2', '3','4', '5',None,None],
    ['6', '7', '8', '9', '0', 'enter'],
    [None, None, None, None, None, None],
    ['space', '<', '^', 'v', '>']
    ]

# Short tab
shortcuts = [
    ['CAP', 'Char', 'Pun', 'Num', 'Short','','delete'],
    [None, 'All', 'Copy', 'Paste', 'Screen','Cut', None],
    ['F1', 'F2', 'F3', 'F4', 'F5', 'enter'],
    ['F12', 'F6', 'F7', 'F8', 'F9', None],
    ['space', '<', '^', 'v', '>']
    ]

# Position of Computer's origin keyboard
bindings = [
    [K_7, K_8, K_9, K_0, K_MINUS, K_PLUS, K_BACKSPACE],
    [K_u, K_i, K_o, K_p, K_LEFTBRACKET, K_RIGHTBRACKET, K_BACKSLASH],
    [K_j, K_k, K_l, K_SEMICOLON, K_QUOTE, K_RETURN],
    [K_n, K_m, K_COMMA, K_PERIOD, K_SLASH, K_TAB],
    [K_SPACE, K_LEFT, K_UP, K_DOWN, K_RIGHT]
]

# Size of each keys in keyboard interface
layout = [
    [(82, 33), (82, 33), (82, 33), (82, 33), (82, 33), (82, 33), (124, 33)],
    [(88, 65), (88, 65), (88, 65), (88, 65), (88, 65), (88, 65), (88, 65)],
    [(91, 65), (91, 65), (91, 65), (91, 65), (91, 65), (170, 65)],
    [(89, 65), (89, 65), (89, 65), (89, 65), (89, 65), (180, 65)],
    [(445, 65), (66, 28), (66, 28), (66, 28), (66, 28)],
    ]


#Tab name for each keyboard (use string since list is a unhashable type)
tab_and_keyboard = {str(keyboard): "Char",
                    str(punctuation): "Pun",
                    str(numbers): "Num",
                    str(shortcuts): "Short"}


pygame.init()
display = pygame.display.set_mode((1200, 350))
pygame.display.set_caption("S-Keyboard")
Clock = pygame.time.Clock() #pygame time for fps
pygame.scrap.init()         #to copy and paste things to clipboard


class Game:
    running = True      # If the game is running
    keyboard = keyboard # the actual keyboard (from beginning: keyboard)
    pressed = {}        # keys that are pressed: {Key-Number: Bool} --> if False: first key, if True: use second key
    text = ""           # the current text
    capslock = False    # if capslock is activated
    cursorpos = [0,0]   # The position of the text cursor: [line, character]
    allselected = False # If the whole text is selected

    def __init__(self,
                 font_family = "",
                 font_size = 50,
                 antialias = True,
                 text_color = (0,0,0),      #color of the text window
                 key_color = (255,255,255), #color of the keys text
                 fps=60):

        #Set class variables
        display.fill((255,255,255))         #at the begining: fill the screen with
                                            # a white color to draw new content to it (like reset)
        self.antialias = antialias
        self.text_color = text_color
        self.key_color = key_color
        self.font = pygame.font.SysFont(font_family, font_size)
        self.keyfont = pygame.font.SysFont("", 25)
        self.fps = fps

        pygame.key.set_repeat(150, 150)     #Set the standard key delays: set_repeat(delay, interval)
                                            # in milliseconds--> 250 means a half second



    def updateKeyboard(self, pressed):
        """
        This function to update/render the keyboard

        CAP key colour into green
        Handle CAP function.
        Input: pressed = dictionary of pressed keys given by pygame.key.get_pressed()
        """
        y = 10              #y-position of the key
        for row in layout:
            x = 10          #x-position of the key
            index = 0       #index of the key in a row (because there can be more same keys in a list
            for key in row:
                ynow = y    #"now" variables, because they change if specific keys (for example arrow keys).
                            # They don't influence the global position variable
                xnow = x
                text = self.keyboard[layout.index(row)][index] #the key text

                #Special set up for arrow keys
                if text in ("<", "v", ">"):
                    ynow += 33
                    if text != "<":
                        xnow -= 66+margins[0]
                
                binding = bindings[layout.index(row)][index] #the key binding
                if binding and pressed[binding]:
                    if self.pressed[binding] and type(text) is tuple:
                        rect = pygame.draw.rect(display, (150,100,100), (xnow, ynow, *key)) #display red when pressed longer (means {key-number: True})
                    else:
                        rect = pygame.draw.rect(display, (100,100,100), (xnow, ynow, *key)) #display key white

                elif text == "CAP" and self.capslock:       #display caps lock key green when activated
                    rect = pygame.draw.rect(display, (100,200,100), (xnow, ynow, *key))

                else:
                    rect = pygame.draw.rect(display, (25,25,25), (xnow, ynow, *key))        #standard dark grey key
                    
                if text:
                    if type(text) is tuple: # lowercase letters if not capslock (if its a list)
                        if not self.capslock:
                            text = [x.lower() for x in text]
                        render1 = self.keyfont.render(text[0], self.antialias, self.key_color)  # White Key  = key 1
                        render2 = self.keyfont.render(text[1], self.antialias, (255,100,0))     # Orange Key = Key 2
                        display.blit(render1, render1.get_rect(centerx=rect.centerx, centery=rect.centery-15)) #center key 1
                        display.blit(render2, render2.get_rect(centerx=rect.centerx, centery=rect.centery+15)) #center key 2
                        
                    else:
                        #Sets the text color
                        textcolor = self.key_color
                        #If it's the actual tab key, change the color to yellow
                        if tab_and_keyboard[str(self.keyboard)] == text: # make it as string because list is a unhashable type!
                            textcolor = 255,255,0
                            
                        if not self.capslock and len(text) == 1:        # lowercase letters if not capslock (if its a single character)
                            text = text.lower()
                        render = self.keyfont.render(text, self.antialias, textcolor) #render key text
                        display.blit(render, render.get_rect(center=rect.center)) #center key text
                x += key[0]+margins[0]  #add key width and defined x margin to x position for the next key
                index += 1              #add 1 to index of the key in the row
            y += row[0][1]+margins[1]   #add row height and defined y margin to y position for the next row


    def update(self):
        """
        Assigning Swifting tab layout.
        Functioning Arrow keys, Enter, Space and Delete

        Created short cut keys = Select all, copy, paste, screenshot and cut
        Drawing cursor and set cursor position (Text window)

        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False        #set running to False to stop the loop

            elif event.type == KEYDOWN:     #if a key is pressed/triggered
                if event.key in bindings[0] or event.key in bindings[-1]: #if key in control keys (arrows and caps, num, etc...)
                    if event.key == bindings[0][0]:
                        self.capslock = not self.capslock   #toggle caps lock
                    elif event.key == bindings[0][1]:
                        self.keyboard = keyboard            #set default keyboard
                    elif event.key == bindings[0][2]:
                        self.keyboard = punctuation         #set punctuation keyboard
                    elif event.key == bindings[0][3]:
                        self.keyboard = numbers             #set number keyboard
                    elif event.key == bindings[0][4]:
                        self.keyboard = shortcuts           #set shortcuts keyboard

                    elif self.text:                         #if any text is written
                        lines = self.text.split("\n")       #split the text by lines

                        #If left key is pressed
                        if event.key == bindings[-1][1]:
                            if self.cursorpos[1] > 0:
                                self.cursorpos[1] -= 1      #move cursor one left
                            elif self.cursorpos[0]:         #move cursor to the line above if theres no character left
                                self.cursorpos[0] -= 1
                                self.cursorpos[1] = len(lines[self.cursorpos[0]])

                        #If up key is pressed
                        elif event.key == bindings[-1][2]:
                            if self.cursorpos[0]:
                                self.cursorpos[0] -= 1
                                self.cursorpos[1] = len(lines[self.cursorpos[0]])
                            else:
                                self.cursorpos = [0,0]

                        #If down key is pressed
                        elif event.key == bindings[-1][3]:
                            if self.cursorpos[0] < len(lines)-1:
                                self.cursorpos[0] += 1
                                self.cursorpos[1] = len(lines[self.cursorpos[0]])

                        #If right key is pressed
                        elif event.key == bindings[-1][4]:
                            if self.cursorpos[1] < len(lines[self.cursorpos[0]]):
                                self.cursorpos[1] += 1
                            elif self.cursorpos[0] < len(lines)-1:
                                self.cursorpos[0] += 1
                                self.cursorpos[1] = 0
                            
                    self.pressed[event.key] = False     # remote the key from the self.pressed dict do not being calculated anymore
                                                        # (to avoid being added to the text) (only if its a control key of course)
                
                elif event.key in self.pressed:         #set key in self.pressed to True (means: first character)
                    self.pressed[event.key] = True
                else:
                    self.pressed[event.key] = False     #if its already in the self.pressed dict and its triggered again,
                                                        # set it to false to tell that the second key is activated
                    
            elif event.type == KEYUP:   #If key is released
                first = None            #first key text
                second = None           #second key text
                for row in bindings:
                    for key in row:
                        if key == event.key:
                            text = self.keyboard[bindings.index(row)][row.index(key)]
                            
                            if type(text) is tuple:
                                first, second = text
                            else:       #special character handling
                                if text == "enter":
                                    text = "\n"
                                elif text == "space":
                                    text = " "
                                elif text in self.keyboard[-1][1:] or text in self.keyboard[0][:-1]:
                                    text = ""
                                first = second = text
                            break

                if first:
                    add = ""        #the text to add
                    lines = self.text.split("\n")
                    line = lines[self.cursorpos[0]]
                    if not self.capslock:       #lowercase letters if not capslock
                        first, second = first.lower(), second.lower()

                    if self.pressed[event.key]: #Second key
                        add = second
                        
                    else:   #First key
                        add = first
                    
                    #Special handling for delete
                    if add == "delete":
                        if self.cursorpos[1]:
                            line = line[:self.cursorpos[1]-1] + line[self.cursorpos[1]:] #remote letter from cursor position
                            lines[self.cursorpos[0]] = line
                            
                        elif self.cursorpos[0]: #jump to above line if theres no character left
                            self.cursorpos[1] = len(lines[self.cursorpos[0]-1])+1
                            lines[self.cursorpos[0]-1] += line
                            del lines[self.cursorpos[0]]


                    #if select all
                    elif add == "all":
                        self.allselected = not self.allselected

                    elif add in ("copy", "cut"): #copy text to clipboard
                        if self.allselected:     #only if text is selected
                            pygame.scrap.put(pygame.SCRAP_TEXT, self.text)

                            if add == "cut":    #if cut, remove also the text from the window
                                lines = []

                            self.allselected = False


                    elif add == "screen":
                        pygame.image.save(display, "screenshot.png")
                                
                            
                    else: #add character on the cursor position
                        pasted = False
                        if add != "paste":
                            self.cursorpos[1] += len(add.replace("\n","")) #replace \n by nothing to stop the cursor to move over invisible characters (like the enter character, etc.)
                        else:
                            add = pygame.scrap.get(pygame.SCRAP_TEXT).replace("\0", "")
                            pasted = True

                        #ignore function keys:
                        if add and add[0].lower() == "f" and add[-1].isdigit():
                            add = ""
                        
                        line = line[:self.cursorpos[1]-1] + add + line[self.cursorpos[1]-1:]
                        lines[self.cursorpos[0]] = line

                        if pasted: self.cursorpos[1] += len(add)
                        
                    
                    self.text = "\n".join(lines) #put lines list to a single text together again
                    

                    if add == "\n":             #change cursor position when hitting ENTER
                        self.cursorpos[0] += 1
                        self.cursorpos[1] = 0
                    elif add == "delete":       #change cursor position when deleting a character
                        if self.cursorpos[1]:   #if characters left, move 1 left
                            self.cursorpos[1] -= 1
                        elif self.cursorpos[0]: #else: jump to line above
                            self.cursorpos[0] -= 1
                        
                del self.pressed[event.key]     #delete key from self.pressed dictionary to avoid multiple triggering

        display.fill((255,255,255))             #fill the screen with a white color to draw new content to it (like reset)
        
        pressed = pygame.key.get_pressed()      #get a dictionary with status of every key
        self.updateKeyboard(pressed)            #update keyboard function

        y = 10 #y-position of the displayed text cursor
        lines = self.text.split("\n")           #not splitlines()! because a line with no text isn't listed up!
        for i in lines:
            render = self.font.render(i, self.antialias, self.text_color) #render every line of the text, because multiline render does not allow  in pygame

            #If the whole text is selected, mark it
            if self.allselected:
                pygame.draw.rect(display, (100,100,100), render.get_rect(topleft=(700,y)))
            blitted = display.blit(render, (700, y)) #--> returns pygame.Rect
            y += blitted.height-5             #add the height of the text line - 5 (to reduce margin) for adding the next line

        if self.cursorpos[0] > len(lines)-1: #if the last line was deleted, move cursor to above line to avoid "line not found" error
            self.cursorpos[0] -= 1
            
        if lines:
            #Calculating the cursor position:
            #x: 700 + precalculated width of the text until the cursor position on the current cursor line
            #y: 40 + linesnumber * linesheight
            curspos = [700+self.font.size(lines[self.cursorpos[0]][:self.cursorpos[1]])[0],
                       40+self.cursorpos[0]*(blitted.height-5)]
            pygame.draw.line(display, self.text_color, curspos, (curspos[0], curspos[1]-blitted.height+5), 2) #draw the cursor
        
        pygame.display.flip() #update the screen
        Clock.tick(self.fps)  #keep fps
        

game = Game()           #initialize game class
while game.running:     #run the game while game.running is True
    game.update()
    
pygame.display.quit()   #quit display first for faster closing
pygame.quit()           #uninitialize every pygame module
