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
        self.step = 1000
        self.min_silence = 2000

    def split(self):

        self.sif_borders = []

        silence = 0
        current_start = 0

        listening_for_new_sif = True

        for i in range(0, len(self.signal), self.step):

            avg_signal_amplitude = np.average(self.signal[i:i + self.step] ** 2)
            self.signal_lr[i:i + self.step] = avg_signal_amplitude

            if listening_for_new_sif and avg_signal_amplitude > self.threshold:
                # self.sif_starts.append(i)
                current_start = i
                listening_for_new_sif = False

            if not listening_for_new_sif and avg_signal_amplitude < self.threshold:
                self.sif_borders.append([current_start, i])
                listening_for_new_sif = True

        sifs = []

        for i in range(len(self.sif_borders)):

            previous_sif_end = self.sif_borders[i - 1][1] + self.step if i > 0 else 0
            future_sif_start = self.sif_borders[i + 1][0] - self.step if i < len(self.sif_borders) - 1 else len(self.signal)

            middle_point = (self.sif_borders[i][0] + self.sif_borders[i][1]) // 2
            start_index = max(previous_sif_end, middle_point - self.sample_rate // 2)

            end_index = min(future_sif_start, middle_point + self.sample_rate // 2)

            sif = np.zeros([self.sample_rate])

            sif[self.sample_rate // 2 - (middle_point - start_index):self.sample_rate // 2 + (end_index - middle_point)] = \
                self.signal[start_index:end_index]

            print("Sif len: {}, Range: {} - {} - {}".format(len(sif), start_index, middle_point, end_index))

            sifs.append(sif)


        return sifs

    def visualize(self):

        plt.plot(self.signal ** 2, label='signal')

        for i in self.sif_borders:
            plt.axvline(x=i[0], color='y')
            plt.axvline(x=i[1], color='g')

        plt.axhline(y=self.threshold, color='r')

        plt.show()

