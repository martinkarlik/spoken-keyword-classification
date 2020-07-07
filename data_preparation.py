import json
import os
import librosa
import numpy as np

DATASET_PATH = "digit_dataset"
JSON_PATH = "digit_dataset/data.json"
SAMPLE_SIZE = 22050


def prepare_dataset(dataset_path, json_path, n_mfcc=13, hop_length=512, n_fft=2048):

    data = {
        "mappings": [],
        "MFCC": [],
        "labels": [],
        "files": []
    }

    for i, dirname in enumerate(sorted(os.listdir(dataset_path))):

        data["mappings"].append(dirname)
        dirpath = os.path.join(dataset_path, dirname)

        print("Processing {}.".format(dirpath))

        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)

            signal, sample_rate = librosa.load(filepath)

            if len(signal) >= 22050:
                signal = signal[:SAMPLE_SIZE]
                mfcc = librosa.feature.mfcc(signal, sample_rate, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=n_fft)

                data["MFCC"].append(mfcc.T.tolist())
                data["labels"].append(i)
                data["files"].append(filepath)

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    prepare_dataset(DATASET_PATH, JSON_PATH)
    # with open(JSON_PATH, "r") as file:
    #     data = json.load(file)
    #
    # data["labels"] = (np.array(data["labels"]) - 1).tolist()
    #
    # with open(JSON_PATH, "w") as file:
    #     json.dump(data, file, indent=4)
