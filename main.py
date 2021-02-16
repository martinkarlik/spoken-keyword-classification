import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from real_time_sif_extractor import *
from audio_io import *

if __name__ == "__main__":

    recording_thread = RecordingThread()
    recording_thread.start()
    rtse = RealTimeSifExtractor()

    recording = True

    while recording:
        data = recording_thread.get_signal_power()

        if len(data) > 0 and rtse.tooLoud(data):
            print("Too loud.")
            recording = False

