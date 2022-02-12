import pyaudio
import wave
 
FILE_PATH = "filename.wav"
CHUNK = 1024
 
wf = wave.open(FILE_PATH, 'rb')
 
print("==================")
# instantiate PyAudio (1)
p = pyaudio.PyAudio()
# open stream (2)

device_count = p.get_device_count()
for i in range(0, device_count):
    print("Name: " + p.get_device_info_by_index(i)["name"])
    print("Index: " + p.get_device_info_by_index(i)["index"])
    print("\n")

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
 
print("p.get_default_input_device_info()")
print(p.get_default_input_device_info())
# read data
data = wf.readframes(CHUNK)
 
# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)
 
# stop stream (4)
stream.stop_stream()
stream.close()
 
# close PyAudio (5)
p.terminate()