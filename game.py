from keras.models import load_model
import cv2
import numpy as np
from random import choice
from sys import exit

innings = 0
player_record = []

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

# Function for retrieving rev_class_map name
def mapper_rev(val):
    global rev_class_map
    return rev_class_map[val]

# Function for retreiving class_map name
def mapper(val):
    global class_map
    return class_map[val]

# Function for giving the player Choice
def choose():
    global player_ch, innings
    innings += 1
    ch = int(input('''\t1. Batting,
          2. Bowling
          3. Exit :'''))
    
    if ch == 1: 
        player_ch = 'Batting'
        return 'Batting'
    elif ch == 2:
        player_ch = 'Bowling'
        return 'Bowling'
    elif ch == 3:
        exit()
    else:
        print("Invalid Choice...Try Again\n\n")
        choose()

# Function for Scoring
def score(play, val):
    global player_score, computer_score
    if play == 'Player':
        player_score += int(val)
    if play == 'Computer':
        computer_score += int(val)

# Function for out or not
def wicket(player, computer):
    if player == computer:
        return True
    return False

# Function for calculating the winner
def calculate_winner(player, computer):
    if player > computer:
        return 'Player'
    elif player < computer:
        return 'Computer'
    else:
        return 'Tie'

# Function for restarting the game
def restart(n):
    if n == -1:
        y_n = input('''Wanna Start Again??? ( The progress won't be saved. )
                                        Y / N ?''')
    if n == 0:
        y_n = input('''Wanna Start Again???
                            Y / N ?''')
    
    if y_n.upper() not in ['Y', 'N']:
        print('''Invalid Choice....Try Again !!!''')
        restart(n)
    
    return y_n.upper()


# Bat / Ball choice
player_ch = ''
print(choose())

model = load_model("Hand-Cricket-model.h5")


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

player_score, computer_score = 0, 0

winner = "none"

# Gameplay Loop
while True:
    ret, frame = cap.read()
    if not ret:
        continue
        
    frame = cv2.flip(frame, 1)
    # PLAYER
    cv2.rectangle(frame, (0, 100), (300, 400), (255, 255, 255), 2)
    # COMPUTER
    cv2.rectangle(frame, (500, 100), (800, 400), (255, 255, 255), 2)
        
    # PLAYER REGION for GESTURE
    roi = frame[100:400, 0:300]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))
    
    # PREDICT MOVE for GESTURE
    pred = model.predict(np.array([img]))
    move_code = np.argmax(pred[0])
    player_move_name = mapper_rev(move_code)
    print(player_move_name)
    
    
    if innings >= 1 and innings < 3:
        if player_ch == 'Batting':
            if player_move_name != 'none':
                computer_move_name = choice(['one','two','three','four','five','six'])
                if wicket(player_move_name, computer_move_name) == True:
                    player_ch = 'Bowling'
                    innings += 1
                else:
                    score('Player', mapper(player_move_name))
                
                if innings == 2:
                    if player_score > computer_score:
                        innings += 1
                        winner = 'Player'
            else:
                computer_move_name = 'none'
                
        
        elif player_ch == 'Bowling':
            if player_move_name == 'none':
                computer_move_name = choice(['one','two','three','four','five','six'])
                if wicket(player_move_name, computer_move_name) == True:
                    player_ch = 'Batting'
                    innings += 1
                else:
                    score('Computer', mapper(computer_move_name))
                    
                if innings == 2:
                    if player_score < computer_score:
                        innings += 1
                        winner = 'Computer'
            else:
                computer_move_name = 'none'
                
    else:
        winner = calculate_winner(player_score, computer_score)
            

    #DISPLAY
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Player: " + str(player_score),
                (5, 50), font, 1.2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Computer: " + str(computer_score),
                (400, 50), font, 1.2, (0, 0, 0), 2, cv2.LINE_AA)
    if winner != 'none':
        cv2.putText(frame, "Winner: "+ winner,
                    (400, 600), font, 2, (0,0,255), 4, cv2.LINE_AA)
     
    
    if computer_move_name == "none":
        pass
    else:
        icon = cv2.imread("{}.jpg".format(computer_move_name))
        icon = cv2.resize(icon, (380, 300))
        frame[100:400, 500:880] = icon
    
    
    cv2.imshow("Cricket is Live ( Player v/s Computer )", frame)
    
    k = cv2.waitKey(10)
    if k == ord("q"):
        exit_q = input('''You Sure??? ( Y/N ) ''')
        if  exit_q.upper() == 'Y':
            break
        else:   continue
    elif k == ord("r"):
        re_start = restart(-1)
        if re_start == 'Y':
            choose()
            player_score, computer_score, innings = 0, 0, 0
        else:
            continue
    elif innings == 3:
        re_start = restart(0)
        if re_start == 'Y':
            choose()
            player_score, computer_score, innings = 0, 0, 0
        else:
            break

cap.release()
cv2.destroyAllWindows()
    
    
