import cv2
import os
import sys
import numpy as np

try:
    label_name = sys.argv[1]
    num_samples = int(sys.argv[2])
    '''label_name = 'hello'
    num_samples = 50'''
except:
    print("Arguments missing.\n")
    print("""Steps for starting video capture (gathering_images.py):
          1. Open cmd
          2. Go to the directory with Program
          3. type -> python gather.py <label name> <number of images>
          
          NOTE: Press "a" to start Capture.
                Press "q" to stop capture.
          """)
    exit(-1)
    
save_path = 'D:/PYTHON/Resume Proj/Hand Cricket/Image_Data'
img_class_path = os.path.join(save_path, label_name)

try:
    os.mkdir(save_path)
except FileExistsError:
    pass
try:
    os.mkdir(img_class_path)
except FileExistsError:
    print("{} directory already exists.".format(img_class_path))
    print("All images gathered will be saved along with existing items in this folder")

cap = cv2.VideoCapture(0)
start = False
count = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    if not ret:
        continue
    
    if count == num_samples:
        break
    
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)

    if start:
        roi = frame[100:500, 100:500]
        save_path = os.path.join(img_class_path, '{}.jpg'.format(count+1))
        cv2.imwrite(save_path, roi)
        count += 1
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Collecting...{}".format(count),
                (400, 80), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting Images", frame)
    
    k = cv2.waitKey(10)
    if k == ord("a"):
        start = not start
    if k == ord("q"):
        break


print("\n{} image(s) saved to {}".format(count, img_class_path))
cap.release()
cv2.destroyAllWindows()


































































