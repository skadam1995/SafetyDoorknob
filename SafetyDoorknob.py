import Tkinter as tk
from PIL import Image, ImageTk
import requests
import time
import RPi.GPIO as GPIO
import random
import os
import sys

Button_A = 29 # The GPIO pin the button is attached to
Button_B = 31 # The GPIO pin the button is attached to
Button_C = 33 # The GPIO pin the button is attached to
Button_D = 35 # The GPIO pin the button is attached to
Button_Confirm = 37 # The GPIO pin the button is attached to

Relay_Contact = 38

#//////Setting up the pinmodes///////
GPIO.setmode(GPIO.BCM) #Defines what the numbering scheme is for the pins
GPIO.setup(Button_A, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setting the button as an input and turning on some Pull-up resistors
GPIO.setup(Button_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Button_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Button_D, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Button_Confirm, GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(Relay_Contact, GPIO.OUT) #Making the Relay contact an output.

global usableQuestions
global currentState
global stateStartTime
global picPath
global correctAnswer
global allAnswers

mainFolderPath = "/home/pi/SafetyDoorknob/AllQuestions" #All Level Folders will be in SafetyDoorknob
answersPath = "/home/pi/SafetyDoorknob/DoorknobAnswers.txt"
picPath = "/home/pi/SafetyDoorknob/HomeScreen.jpg"
answers_file = open(answersPath,'r')
allAnswers = answers_file.readline().split(",") #Load all answers into String Array
usableQuestions = os.listdir(mainFolderPath)


root = tk.Tk()
root.geometry("800x480")
root.configure(background = 'black')
root.wm_attributes('-type','splash')

def buttonPressToAnswer():
    currentAnswer = ""
    
    if GPIO.input(Button_A) == 0:
        time.sleep(0.02)
        currentAnswer = "A"
    elif GPIO.input(Button_B) == 0:
        time.sleep(0.02)
        currentAnswer = "B"
    elif GPIO.input(Button_C) == 0:
        time.sleep(0.02)
        currentAnswer = "C"
    elif GPIO.input(Button_D) == 0:
        time.sleep(0.02)
        currentAnswer = "D"

    return currentAnswer


def get_State_Time():

    stateTime = time.time() - stateStartTime
    return int(round(stateTime))

def setState(newState):
    currentState = newState
    stateStartTime = time.time()

def safety_loop():

    if currentState == 0: #Startup State
        picPath = "/home/pi/SafetyDoorknob/HomeScreen.jpg"

        if GPIO.input(Button_Confirm) == 0:
            time.sleep(0.02)
            while GPIO.input(Button_Confirm) == 0:
                pass
            setState(1)
            picPath = pick_rand_img()
        root.after(10,safety_loop)
            
    elif currentState == 1: #Question 1 State
        while get_State_Time() <= 120:
            if buttonPressToAnswer() == correctAnswer:
                break
            else:
                pass
        if get_State_Time() <=120:
            setState(2)
            picPath = pick_rand_img()
        else:
            setState(0)

        root.after(10,safety_loop)
                           
    elif currentState == 2: #Question 2 State
        while get_State_Time() <= 120:
            if buttonPressToAnswer() == correctAnswer:
                break
            else:
                pass
        if get_State_Time() <=120:
            setState(3)
            picPath = pick_rand_img()
        else:
            setState(0)

        root.after(10,safety_loop)
            
    elif currentState == 3: #Question 3 State
        while get_State_Time() <= 120:
            if buttonPressToAnswer() == correctAnswer:
                break
            else:
                pass
        if get_State_Time() <=120:
            setState(4)
            picPath = pick_rand_img()
        else:
            setState(0)

        root.after(10,safety_loop)
            
    elif currentState == 4: #Door Open State

        GPIO.output(Relay_Contact,1)
        time.sleep(60)
        GPIO.output(Relay_Contact,0)
        
    
def pick_rand_img():

    if len(usableQuestions) == 0:

        usableQuestions = os.listdir(mainFolderPath)
        

    randomIndex = random.randint(0,len(usableQuestions) - 1)
    randQuestion = usableQuestions[randomIndex] #Picks random question
    correctAnswer = allAnswers[randomIndex]
    
    
    newQuestionPath = mainFolderPath + randQuestion
    usableQuestions.pop(randomIndex)
    allAnswers.pop(randomIndex)

    return newQuestionPath

img = ImageTk.PhotoImage(Image.open(picPath))
panel = tk.Label(root,image = img)

panel.pack(side = "bottom",fill = "both",expand = "yes")
setState(0)
root.after(10,safety_loop)
root.mainloop()
    
    
    
    
    

    
