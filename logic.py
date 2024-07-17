# import the necessary libraries
import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3

# Calculator button class
class CalculatorButton:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
    
    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (125,125,125), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50,50,50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (50,50,50), 2)
        
    def isClicked(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
           self.pos[1] < y < self.pos[1] + self.height:
            return True
        return False
    
# Initialize pyttsx3 engine for speech synthesis
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Launching Virtual Calculator, please wait...")
engine.runAndWait()

# Defining calculator buttons
buttons = [['7', '8', '9', 'C'],
           ['4', '5', '6', '*'],
           ['1', '2', '3', '+'],
           ['0', '-', '/', '='],
           ['(', ')', '.', 'del']]

buttonList = []
for y, row in enumerate(buttons):
    for x, button in enumerate(row):
        xpos = x * 100 + 700
        ypos = y * 100 + 100
        buttonList.append(CalculatorButton((xpos, ypos), 100, 100, button)) # width, height, label pf button

#Initializing variables for Calculator
Equation = ''
Counter = 0  

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.9, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    #Drawing calculator buttons
    for button in buttonList:
        button.draw(img)

    #Checking for hand gestures
    if hands:
        lmList = hands[0]['lmList'] # get landmark list for first hand

        if len(lmList) >= 13:
            # Calculate distance between index and middle fingers
            length, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

            # click detection
            x, y = lmList[8][:2]
            if length < 50 and Counter == 0:
                for button in buttonList:
                    if button.isClicked(x, y):
                        myValue = button.value
                        if myValue == '=':
                            try:
                                Equation = str(eval(Equation))
                            except:
                                print("Syntax error")
                                engine.say("Syntax error")
                                engine.runAndWait()
                                Equation = 'Syntax Error'
                        elif myValue == 'C':
                            Equation = ''
                        elif myValue == 'del':
                            Equation = Equation[:-1]
                        else:
                            Equation += myValue
                        Counter = 1

    # Delay to prevent multiple clicks
    if Counter != 0:
        Counter += 1
        if Counter > 10:
            Counter = 0
    
    # Displaying calculator equation
    cv2.rectangle(img, (700, 20), (1100, 100), (175, 125, 155), cv2.FILLED)
    cv2.rectangle(img, (700, 20), (1100, 100), (50, 50, 50), 3)
    cv2.putText(img, 'VIRTUAL CALCULATOR', (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv2.putText(img, Equation, (710, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # Show the frame
    cv2.imshow("Virtual Calculator", img)
    cv2.moveWindow("Virtual Calculator", 0, 0)

    # Close the webcam
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()