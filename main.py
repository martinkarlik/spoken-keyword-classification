import sounddevice as sd
from digit_spotting_service import *
from sif_splitting_service import *

SAMPLE_RATE = 22050


if __name__ == "__main__":


    sd.default.channels = 1
    sd.default.samplerate = SAMPLE_RATE

    print("Recording...")
    signal = sd.rec(SAMPLE_RATE * 5)
    sd.wait()
    print("Stopped")

    print("Playing...")
    sd.play(signal)
    sd.wait()
    print("Stopped")

    signal = signal[SAMPLE_RATE:, 0]

    sss = SifSplittingService(signal, SAMPLE_RATE)
    dss = DigitSpottingService()

    sifs = sss.split()
    sss.visualize()

    print("This many sifs: {}".format(len(sifs)))

    for sif in sifs:
        sd.play(sif)
        sd.wait()
        digit = dss.predict(sif, SAMPLE_RATE)
        # print("I think that the digit is {}.".format(digit))




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