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
        self.rec_data = np.array([])

        self.rec_stream = sd.InputStream(samplerate=self.sampling_freq, channels=1, blocksize=self.chunk_samples,
                                         callback=self.callback)

    def callback(self, indata, frames, time, status):
        if self.rec_data.size == 0:
            self.rec_data = indata
        else:
            self.rec_data = np.append(self.rec_data, indata, axis=0)

    def run(self):
        self.rec_stream.start()

    def stop(self):
        self.rec_stream.stop()
        self.rec_data = np.array(self.rec_data)

    def get_data(self):
        return self.rec_data

    def set_data(self, rec_data):
        self.rec_data = rec_data


class PlaybackThread(AudioIOThread):

    def __init__(self):
        super().__init__()


class DynamicPlaybackThread(PlaybackThread):

    def __init__(self):
        super().__init__()

        self.play_stream = sd.OutputStream(samplerate=self.sampling_freq, channels=2, blocksize=self.chunk_samples,
                                           callback=None)

    def run(self):
        self.play_stream.start()

