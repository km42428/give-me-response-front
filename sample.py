# -*- coding:utf-8 -*-

import pyaudio
import numpy as np

CHUNK = 1024
RATE = 44100
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                frames_per_buffer=CHUNK,
                input=True,
                output=True)  # inputとoutputを同時にTrueにする

all = []
def is_talking(array):
  return any(list(array))

# tmpは常に同じ長さ
tmp = [False for k in range(0, 20)]
while stream.is_active():
    input = stream.read(CHUNK)
    npData = np.frombuffer(input, dtype="int16") / 32768.0

		# 声の大きさが閾値を超えると話している判定にする
    threshold = 0.1
    isThresholdOver = False
    if max(npData) > threshold:
        isThresholdOver = True
    
    tmp.append(isThresholdOver)
    tmp.pop(0)
    if (is_talking(tmp)):
      print("お話し中...")
    else:
      print("おしゃべりしましょ")

stream.stop_stream()
stream.close()
p.terminate()

print("Stop Streaming")
