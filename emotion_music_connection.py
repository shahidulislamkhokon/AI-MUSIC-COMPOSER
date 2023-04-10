import os
import wave
import pathlib
import pygame
emotion_list = ['happy','sad']
# song_dir = 'E:/musicgenerator5/emotion_songs/'
add_music = []
for emotion in emotion_list:
    #print(emotion)
    if emotion == 'happy' and os.path.exists('happy.wav'):
        add_music.append('happy.wav')
    elif emotion == 'sad' and os.path.exists('sad.wav'):
        add_music.append('sad.wav')
    else:
        continue

outfile = "sounds.wav"

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

# initial_count = 0
# for path in pathlib.Path('E:/musicgenerator5/emotion_songs').iterdir():
#     if path.is_file():
#         initial_count +=1
# print(initial_count)

