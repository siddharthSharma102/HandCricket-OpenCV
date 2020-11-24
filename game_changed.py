import numpy as np
from sys import exit
import cv2
from random import choice
from keras.models import load_model


innings = ""
p_score = 0
c_score = 0

rev_class_map = {
    0:"none",
    1:"one",
    2:"two",
    3:"three",
    4:"four",
    5:"five",
    6:"six"
    }

class_map = {
    "none":0,
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6
    }

innings_map = {
    1:"First",
    2:"Second",
    3:"End"}

rev_innings_map = {
    "First":1,
    "Second":2,
    "End":3}

def mapper(val):
    global class_map
    return int(class_map[val])

def rev_mapper(val):
    global rev_class_map
    return str(rev_class_map[val])

def choose():
    global innings
    ch = int(input("""\tPlayers Choice:
         1. Batting
         2. Balling
         3. Exit: """))
    
    if ch == 1:
        innings = "First"
        return str("Batting")
    elif ch == 2:
        innings = "First"
        return str("Balling")
    elif ch == 3:
        exit()
    else:
        print("Invalid Choice .... Try Again")
        choose()

def batting(c_move, p_move):
    global p_score, class_map, innings
    
    if p_move == c_move:
        innings = innings_map[rev_innings_map[innings] + 1]
        return p_score
    p_score += class_map[p_move]
    return p_score
        
def balling(c_move, p_move):
    global c_score, class_map, innings
    
    if p_move == c_move:
        innings = innings_map[rev_innings_map[innings] + 1]
        return c_score
    c_score += class_map[c_move]
    return c_score
    
def winner_bat(p_score, c_score):
    if p_score > c_score:
        return "P"

def winner_ball(p_score, c_score):
    if p_score < c_score:
        return "C"


# CHOOSING BAT OR BALL
p_turn = choose()
print("You Choose {}".format(p_turn))

# LOAD TRAINED MODEL
model = load_model("Hand-Cricket-model.h5")

# START VIDEO CAPTURE
cap = cv2.VideoCapture(0)

c_move = "none"
p_pre_move = "none"
c_pre_move = "none"
# GAME LOOP
while True:
    ret, frame = cap.read()
    
    # PLAYER BOX
    cv2.rectangle(frame, (0, 30), (300, 330), (255, 255, 255), 2)
    # COMPUTER BOX
    cv2.rectangle(frame, (330, 170), (630, 470), (255, 255, 255), 2)
    
    roi = frame[30:330, 0:300]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))
        
    # PREDICT MOVE for GESTURE
    pred = model.predict(np.array([img]))
    move_code = np.argmax(pred[0])
    p_move = rev_mapper(move_code)
    print(p_move, "\t", c_move)
    
    if p_pre_move != "none":
        pass
    else:
        if innings == 'First':
            if p_turn == 'Batting' and p_move != "none":
                c_move = choice(["one", "two", "three", "four", "five", "six"])
                p_score = batting(c_move, p_move)
            if p_turn == 'Balling' and p_move != "none":
                c_move = choice(["one", "two", "three", "four", "five", "six"])
                c_score = balling(c_move, p_move)
                
        elif innings == 'Second':
            if p_turn == 'Batting' and p_move != "none":
                c_move = choice(["one", "two", "three", "four", "five", "six"])
                p_score = batting(c_move, p_move)
                win = winner_bat(p_score, c_score)
                if win == "P":
                    print("Player Won the match by {} run".format(p_score - c_score))
                    break
            else:
                c_move = choice(["one", "two", "three", "four", "five", "six"])
                c_score = balling(c_move, p_move)
                win = winner_ball(p_score, c_score)
                if win == "C":
                    print("Computer Won the Match by {} runs".format(c_score - p_score))
                    break
    p_pre_move = p_move
    
    
    if c_move == "none":
        pass
    else:
        icon = cv2.imread("{}.png".format(c_move))
        icon = cv2.resize(icon, (300, 130))
        frame[350:650, 170:470] = icon
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, innings + " Inning",
                (500, 30), font, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, "Player: " + str(p_score),
                (5, 360), font, 0.7, (255, 0, 0), 2)
    cv2.putText(frame, "Computer: " + str(c_score),
                (5, 390), font, 0.7, (0, 0, 255), 2)
    
    cv2.imshow("Cricket is Live ( Player v/s Computer )", frame)
    
    k = cv2.waitKey(10)
    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
