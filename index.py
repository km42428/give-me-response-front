import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import pyaudio
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import asyncio

app = Flask(__name__)
bootstrap = Bootstrap(app)

CHUNK = 1024
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                frames_per_buffer=CHUNK,
                input=True,
                output=True)  # inputとoutputを同時にTrueにする
tmp = [False for k in range(0, 100)]

def is_talking(array):
    return any(list(array))


# 音声取得
def audio():
    while stream.is_active():
        input = stream.read(CHUNK, exception_on_overflow=False)
        npData = np.frombuffer(input, dtype="int16") / 32768.0
        # 声の大きさが閾値を超えると話している判定にする
        threshold = 0.1
        isThresholdOver = False
        if max(npData) > threshold:
            isThresholdOver = True
        tmp.append(isThresholdOver)
        tmp.pop(0)

scheduler = BackgroundScheduler()  # スケジューラを作る
scheduler.add_job(audio, 'interval', seconds=3)  # ジョブを追加
scheduler.start()  # スタート

@app.route('/')
def hello_world():
    return render_template("index.html", is_talking=True)

@app.route('/audio')
def get_audio():
    return dict(is_talking=is_talking(tmp))

if __name__ == '__main__':
    app.run()
