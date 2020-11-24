from keras.models import load_model
import cv2
import numpy as np
import sys

filepath = sys.argv[1]
#filepath = 'test_one.jpg'

rev_class_map = {
    0:"none",
    1:"one",
    2:"two",
    3:"three",
    4:"four",
    5:"five",
    6:"six"}


def mapper(val):
    return rev_class_map[val]

# LOADNG TRAINED MODEL
model = load_model("Hand-Cricket-model.h5")

# PREPARING IMAGE
img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (227, 227))

# PREDICTION
pred = model.predict(np.array([img]))
move_code = np.argmax(pred[0])
move_name = mapper(move_code)

print("\n\nPridcted: {}".format(move_name))
