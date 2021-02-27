import tensorflow.keras as keras
import numpy as np
import librosa

MODEL_PATH = "models/model.h5"

SAMPLES_TO_CONSIDER = 22050


class _DigitSpottingService:
    model = None

    _mappings = [i for i in range(1, 9)]
    instance = None

    def predict(self, signal, sr):

        signal_to_consider = np.zeros(SAMPLES_TO_CONSIDER)

        if len(signal) < SAMPLES_TO_CONSIDER:
            signal_to_consider[:len(signal)] = signal
        else:
            signal_to_consider = signal[:SAMPLES_TO_CONSIDER]

        mfcc = librosa.feature.mfcc(signal_to_consider, sr, n_mfcc=13, n_fft=2048, hop_length=512).T
        mfcc = mfcc[np.newaxis, ..., np.newaxis]


        predictions = self.model.predict(mfcc)
        prediction_index = np.argmax(predictions)

        # print("I think it's {} ({})".format(self._mappings[prediction_index], predictions[0, prediction_index]))

        return self._mappings[prediction_index], predictions[0, prediction_index]


def DigitSpottingService():

    if _DigitSpottingService.instance is None:
        _DigitSpottingService.instance = _DigitSpottingService()
        _DigitSpottingService.model = keras.models.load_model(MODEL_PATH)

    return _DigitSpottingService.instance



