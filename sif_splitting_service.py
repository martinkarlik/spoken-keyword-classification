# import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import librosa


class SifSplittingService:

    def __init__(self, signal, sample_rate):
        self.signal = signal
        self.signal_lr = np.zeros(len(self.signal))

        self.sample_rate = sample_rate
        self.sif_starts = []

        self.threshold = np.average(self.signal**2)
        self.step = 2000
        self.min_silence = 2000

    def split(self):

        self.sif_starts = []

        silence = 0
        listening_for_new_sif = False

        for i in range(0, len(self.signal), self.step):

            avg_signal_amplitude = np.average(self.signal[i:i + self.step] ** 2)
            self.signal_lr[i:i + self.step] = avg_signal_amplitude

            if listening_for_new_sif and avg_signal_amplitude > self.threshold:
                self.sif_starts.append(i)
                listening_for_new_sif = False

            if avg_signal_amplitude < self.threshold:
                listening_for_new_sif = True

        sifs = []

        for i in self.sif_starts:
            if i + self.sample_rate > len(self.signal):
                sif = self.signal[i:len(self.signal)]
            else:
                sif = self.signal[i:i+self.sample_rate]

            sifs.append(sif)

        return sifs

    def visualize(self):

        plt.plot(self.signal ** 2, label='signal')

        for i in self.sif_starts:
            plt.axvline(x=i, color='y')

        plt.axhline(y=self.threshold, color='r')

        plt.show()

