import pydub
import numpy as np
import librosa
import audioread


def load_GAN_Y(length):
    y = np.ones([length, 1])
    return y

def load_Discr_Y(length, gan_output=False):
    if gan_output:
        y = np.zeros([length, 1])
    else:
        y = np.ones([length, 1])

    return y


def load_correct_disc_X(audio_file_path, time_stamps):
    with audioread.audio_open(audio_file_path) as f:
        correct_cuts = []

    for word in time_stamps:

        new_cut = librosa.load(audio_file_path, offset=start, duration=3)[0]
        correct_cuts.append(new_cut)

    return correct_cuts
