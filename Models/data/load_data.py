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
        duration = int(f.duration)

    correct_cuts = []

    for word in time_stamps:
        if word.success() and word.start>1.3 and word.end<duration-2:
            new_cut = librosa.load(audio_file_path, offset=word.start-1.2, duration=3)[0]
            correct_cuts.append(new_cut)

    return correct_cuts


