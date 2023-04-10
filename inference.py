import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
import os
import wave
from time import strftime


    
model  = load_model("model.h5")
label = np.load("labels.npy")

#store all landmarks postion on X
X = []
data_size = 0

holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

# cap = cv2.VideoCapture(0)
#########full screen##########

# import cv2
# import ctypes
#
# WINDOW_NAME = 'Full Integration'

# initialize video capture object to read video from external webcam
cap = cv2.VideoCapture(0)
# if there is no external camera then take the built-in camera
# if not video_capture.read()[0]:
#     video_capture = cv2.VideoCapture(0)

# Full screen mode
# cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# while (cap.isOpened()):
#     # get Screen Size
#     user32 = ctypes.windll.user32
#     screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#
#     # read video frame by frame
#     ret, frame = cap.read()
#
#     frame = cv2.flip(frame, 1)
#
#     frame_height, frame_width, _ = frame.shape
#
#     scaleWidth = float(screen_width) / float(frame_width)
#     scaleHeight = float(screen_height) / float(frame_height)
#
# if scaleHeight > scaleWidth:
#     imgScale = scaleWidth
#
# else:
#     imgScale = scaleHeight
#
# newX, newY = frame.shape[1] * imgScale, frame.shape[0] * imgScale
# frame = cv2.resize(frame, (int(newX), int(newY)))
# cv2.imshow(WINDOW_NAME, frame)

##############################


pre_lsit = []
while True:
    lst = []

    _, frm = cap.read()

    frm = cv2.flip(frm, 1)

    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))


    if res.face_landmarks:
        for i in res.face_landmarks.landmark:
            lst.append(i.x - res.face_landmarks.landmark[1].x)
            lst.append(i.y - res.face_landmarks.landmark[1].y)

        if res.left_hand_landmarks:
            for i in res.left_hand_landmarks.landmark:
                lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                lst.append(0.0)

        if res.right_hand_landmarks:
            for i in res.right_hand_landmarks.landmark:
                lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                lst.append(0.0)

        X.append(lst)
        data_size = data_size + 1

        lst = np.array(lst).reshape(1,-1)

        pred = label[np.argmax(model.predict(lst))]
        pre_lsit.append(pred)
        # cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)

    # print(pre_lsit)
    drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_CONTOURS)
    drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
    drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)

    # cv2.putText(frm, str(data_size), (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #cv2.putText(frm, strftime("::%S"), (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("window", frm)


    if cv2.waitKey(50) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break

print(pre_lsit)
############################
#    Emotion selection
############################
angry = 0
confused = 0
excited = 0
happy = 0
joyful = 0
nervous = 0
neutral = 0
sad = 0
scared = 0
shocked = 0
silly = 0
sleepy = 0
emotion_list = []
for i in range(len(pre_lsit)):
    if pre_lsit[i] == 'angry':
        angry += 1
    elif pre_lsit[i] == 'confused':
        confused += 1
    elif pre_lsit[i] == 'excited':
        excited += 1
    elif pre_lsit[i] == 'happy':
        happy += 1
    elif pre_lsit[i] == 'joyful':
        joyful += 1
    elif pre_lsit[i] == 'nervous':
        nervous += 1
    elif pre_lsit[i] == 'neutral':
        neutral += 1
    elif pre_lsit[i] == 'sad':
        sad += 1
    elif pre_lsit[i] == 'scared':
        scared += 1
    elif pre_lsit[i] == 'shocked':
        shocked += 1
    elif pre_lsit[i] == 'silly':
        silly += 1
    elif pre_lsit[i] == 'sleepy':
        sleepy += 1
    else:
        continue

if angry > (60//2):
    emotion_list.append('angry')
if confused > (60//2):
    emotion_list.append('confused')
if excited > (60//2):
    emotion_list.append('excited')
if happy > (60//2):
    emotion_list.append('happy')
if joyful > (60//2):
    emotion_list.append('joyful')
if nervous > (60//2):
    emotion_list.append('nervous')
if neutral > (60//2):
    emotion_list.append('neutral')
if sad > (60//2):
    emotion_list.append('sad')
if scared > (60//2):
    emotion_list.append('scared')
if shocked > (60//2):
    emotion_list.append('shocked')
if silly > (60//2):
    emotion_list.append('silly')
if sleepy > (60//2):
    emotion_list.append('sleepy')



print(emotion_list)
# ############################
#      #music addition
# ############################
add_music = []
for emotion in emotion_list:
    if emotion == 'angry' and os.path.exists('angry.wav'):
        add_music.append('angry.wav')
    elif emotion == 'confused' and os.path.exists('confused.wav'):
        add_music.append('confused.wav')
    elif emotion == 'excited' and os.path.exists('excited.wav'):
        add_music.append('excited.wav')
    elif emotion == 'happy' and os.path.exists('happy.wav'):
        add_music.append('happy.wav')
    elif emotion == 'joyful' and os.path.exists('joyful.wav'):
        add_music.append('joyful.wav')
    elif emotion == 'nervous' and os.path.exists('nervous.wav'):
        add_music.append('nervous.wav')
    elif emotion == 'neutral' and os.path.exists('neutral.wav'):
        add_music.append('neutral.wav')
    elif emotion == 'sad' and os.path.exists('sad.wav'):
        add_music.append('sad.wav')
    elif emotion == 'scared' and os.path.exists('scared.wav'):
        add_music.append('scared.wav')
    elif emotion == 'shocked' and os.path.exists('shocked.wav'):
        add_music.append('shocked.wav')
    elif emotion == 'silly' and os.path.exists('silly.wav'):
        add_music.append('silly.wav')
    elif emotion == 'sleepy' and os.path.exists('sleepy.wav'):
        add_music.append('sleepy.wav')
    else:
        continue

########### combine music ##########

outfile = "AI MUSIC.wav"

data = []
for songs in add_music:
    w = wave.open(songs, 'rb')
    data.append([w.getparams(), w.readframes(w.getnframes())])
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()