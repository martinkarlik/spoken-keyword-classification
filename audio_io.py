import sounddevice as sd
import soundfile as sf
import numpy as np
import threading


class AudioIOThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sampling_freq = 22050
        self.chunk_duration = 0.1
        self.chunk_samples = int(self.sampling_freq * self.chunk_duration)


class RecordingThread(AudioIOThread):

    def __init__(self):
        super().__init__()

        self.session_len = self.sampling_freq // 2
        self.session_index = 0
        self.rec_data = np.zeros([self.session_len])

        self.rec_stream = sd.InputStream(samplerate=self.sampling_freq, channels=1, blocksize=self.chunk_samples,
                                         callback=self.callback)

    def callback(self, indata, frames, time, status):

        self.rec_data[self.session_index:self.session_index + self.chunk_samples] = indata[:, 0]
        self.session_index += self.chunk_samples

        # if self.rec_data.size == 0:
        #     self.rec_data = indata[:, 0]
        # else:
        #     self.rec_data = np.append(self.rec_data, indata, axis=0)[-self.session_len:]

    def run(self):
        self.rec_stream.start()

    def stop(self):
        self.rec_stream.stop()
        self.rec_data = np.array(self.rec_data)

    def retrieve_session(self):
        self.session_index = 0
        return self.rec_data

    def get_signal_power(self):
        return np.power(np.array(self.rec_data), 2)

    def set_data(self, rec_data):
        self.rec_data = rec_data

