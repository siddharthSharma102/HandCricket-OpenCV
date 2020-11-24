import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf
import os

save_path = 'D:/PYTHON/Resume Proj/Hand Cricket/Image_data'
class_map = {"none":0,
             "one":1,
             "two":2,
             "three":3,
             "four":4,
             "five":5,
             "six":6}

num_classes = len(class_map)

def mapper(val):
    return class_map[val]

# MODEL FUNCTION
def getmodel():
    model = Sequential([
        SqueezeNet(input_shape = (227, 227, 3), include_top = False),
        Dropout(0.5),
        Convolution2D(num_classes, (1,1), padding = "valid"),
        Activation("relu"),
        GlobalAveragePooling2D(),
        Activation("softmax")
    ])
    
    return model


dataset = []
for directory in os.listdir(save_path):
    path = os.path.join(save_path, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        dataset.append([img, directory])
    
'''
dataset = [
    [[...], 'none'],
    [[...], 'one'],
    [[...], 'two'],
    ...
    ]
'''

data, labels = zip(*dataset)
labels = list(map(mapper, labels))

labels = np_utils.to_categorical(labels)

model = getmodel()

model.compile(
    optimizer = Adam(lr = 0.0001),
    loss = 'categorical_crossentropy',
    metrics = ['accuracy']
)

model.fit(np.array(data), np.array(labels), epochs = 6)

model.save("Hand-Cricket-model.h5")
