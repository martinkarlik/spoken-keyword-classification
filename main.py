import sounddevice as sd
from audio_io import *
from real_time_sif_extractor import *
from digit_spotting_service import *
from sif_splitting_service import *

SAMPLE_RATE = 22050


if __name__ == "__main__":

    rtse = RealTimeSifExtractor(SAMPLE_RATE)
    dss = DigitSpottingService()

    recording_thread = RecordingThread()
    recording_thread.start()

    recording = True

    while recording:
        signal = recording_thread.get_signal()

        if len(signal) > 0:

            sifs = rtse.extractSifs(signal)

            for sif in sifs:
                digit = dss.predict(sif, SAMPLE_RATE)
                print("I think that the digit is {}.".format(digit))




# sd.default.channels = 1
    # sd.default.samplerate = SAMPLE_RATE
    #
    # print("Recording...")
    # signal = sd.rec(SAMPLE_RATE * 5)
    # sd.wait()
    # print("Stopped")
    #
    # # print("Playing...")
    # # sd.play(signal)
    # # sd.wait()
    # # print("Stopped")
    #
    # signal = signal[SAMPLE_RATE:, 0]
    #
    # sss = SifSplittingService(signal, SAMPLE_RATE)
    # dss = DigitSpottingService()
    #
    # sifs = sss.split()
    # sss.visualize()
    #
    # print("This many sifs: {}".format(len(sifs)))
    #
    # for sif in sifs:
    #     sd.play(sif)
    #     sd.wait()
    #     digit = dss.predict(sif, SAMPLE_RATE)
    #     # print("I think that the digit is {}.".format(digit))