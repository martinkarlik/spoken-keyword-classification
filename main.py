import sounddevice as sd
import librosa
from audio_io import *
from real_time_sif_extractor import *
from digit_spotting_service import *
from sif_splitting_service import *

SAMPLE_RATE = 22050


CONFIDENCE_THRESHOLD_MAP = {1: 0.95, 2: 0.95, 3: 0.95, 4: 0.95, 5: 0.99, 6: 0.9, 7: 0.75, 8: 0.9}


if __name__ == "__main__":

    # rtse = RealTimeSifExtractor(SAMPLE_RATE)
    # dss = DigitSpottingService()
    #
    # recording_thread = RecordingThread()
    # recording_thread.start()
    #
    # recording = True
    #
    # while recording:
    #     if recording_thread.session_index == recording_thread.session_len:
    #         signal = recording_thread.retrieve_session()
    #
    #         sifs = rtse.extractSifs(signal)
    #
    #         for sif in sifs:
    #             digit, confidence = dss.predict(sif, SAMPLE_RATE)
    #             if confidence > 0.95:
    #                 print("I think that the digit is {}.".format(digit))


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

    # signal, sample_rate = librosa.load("datasets/digit_dataset/7/0a0b46ae_nohash_0.wav")


    sss = SifSplittingService(SAMPLE_RATE)
    dss = DigitSpottingService()

    sifs, sif_borders = sss.split(signal)
    sss.visualize(signal, sif_borders)

    print("This many sifs: {}".format(len(sifs)))

    for sif in sifs:
        sd.play(sif)
        sd.wait()
        digit, confidence = dss.predict(sif, SAMPLE_RATE)

        if confidence > CONFIDENCE_THRESHOLD_MAP[digit]:
            print("It's {}. I'm {}% sure.".format(digit, confidence))
