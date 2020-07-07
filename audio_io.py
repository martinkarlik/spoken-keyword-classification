import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

sample_rate = 48000

track, _ = sf.read("letters.wav")
track = np.array(track)
track = np.divide(track, np.max(np.abs(track)))



plt.figure(figsize=(20, 15))
plt.title("Waveform")
plt.plot(np.arange(track.shape[0]), track[:, 0], label="Right ear")
plt.plot(np.arange(track.shape[0]), track[:, 1], label="Left ear")
plt.show()


# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8702300


# Record letters
# sample_rate = 48000
# duration = 20
#
# sd.default.samplerate = sample_rate
# sd.default.channels = 2
# output = sd.rec(sample_rate*duration)
#
# print("Started")
# sd.wait()
# print("Stopped")
#
# sf.write("letters.wav", output, samplerate=sample_rate)
