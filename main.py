import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import librosa
from digit_spotting_service import *
from sif_splitting_service import *

if __name__ == "__main__":

    sd.default.channels = 1
    sd.default.samplerate = 22050

    print("Recording...")
    signal = sd.rec(22050 * 10)
    sd.wait()
    print("Stopped")

    print("Playing...")
    sd.play(signal)
    sd.wait()
    print("Stopped")

    signal = signal[22050:, 0]
    sr = 22050

    # signal, sr = librosa.load("datasets/digit_dataset/3/0c40e715_nohash_1.wav")

    sss = SifSplittingService(signal, sr)
    dss = DigitSpottingService()

    sifs = sss.split()
    sss.visualize()

    print("This many sifs: {}".format(len(sifs)))

    for sif in sifs:
        sd.play(sif)
        sd.wait()
        digit = dss.predict(sif, sr)
        print("I think that the digit is {}.".format(digit))




# recording_thread = RecordingThread()
# recording_thread.start()
# rtse = RealTimeSifExtractor()
#
# recording = True
#
# while recording:
#     data = recording_thread.get_signal_power()
#
#     if len(data) > 0 and rtse.tooLoud(data):
#         print("Too loud.")
#         recording = False