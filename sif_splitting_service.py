# import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import librosa


class SifSplittingService:

    def __init__(self, sample_rate):

        self.sample_rate = sample_rate


    def split(self, signal):

        # signal_lr = np.zeros([len(signal)])

        step = len(signal) // (self.sample_rate * 22)
        min_silence_duration = step * 4
        silence_threshold = np.average(signal ** 2)

        sif_borders = []

        current_start = 0
        listening_for_new_sif = True

        for i in range(0, len(signal), step):

            avg_signal_amplitude = np.average(signal[i:i + step] ** 2)
            # signal_lr[i:i + step] = avg_signal_amplitude

            if listening_for_new_sif and avg_signal_amplitude > silence_threshold:
                current_start = i
                listening_for_new_sif = False

                if len(sif_borders) > 0 and current_start - sif_borders[len(sif_borders) - 1][1] <= min_silence_duration:
                    current_start = sif_borders[len(sif_borders) - 1][0]
                    sif_borders.pop(len(sif_borders) - 1)

            if not listening_for_new_sif and avg_signal_amplitude < silence_threshold or i == len(signal) - step:

                sif_borders.append([current_start, i])
                listening_for_new_sif = True

        sifs = []

        for i in range(len(sif_borders)):

            previous_sif_end = sif_borders[i - 1][1] + step if i > 0 else 0
            future_sif_start = sif_borders[i + 1][0] - step if i < len(sif_borders) - 1 else len(signal)

            middle_point = (sif_borders[i][0] + sif_borders[i][1]) // 2
            start_index = max(previous_sif_end, middle_point - self.sample_rate // 2)
            end_index = min(future_sif_start, middle_point + self.sample_rate // 2)

            sif = np.zeros([self.sample_rate])

            sif[self.sample_rate // 2 - (middle_point - start_index):self.sample_rate // 2 + (end_index - middle_point)] = \
                signal[start_index:end_index]

            print("Sif len: {}, Range: {} - {} - {}".format(len(sif), start_index, middle_point, end_index))

            sifs.append(sif)

        return sifs, sif_borders

    def visualize(self, signal, sif_borders):

        plt.plot(signal ** 2, label='signal')

        for i in sif_borders:
            plt.axvline(x=i[0], color='y')
            plt.axvline(x=i[1], color='g')

        plt.show()

