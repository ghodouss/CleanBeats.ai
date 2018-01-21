import pydub
import numpy as np


def load_GAN_Y(length):
    y = np.ones([length, 1])
    return y

def load_Discr_Y(length, gan_output=False):
    if gan_output:
        y = np.ones([length, 1])*-1
    else:
        y = np.ones([length, 1])

    return y


