from remove_explitives import get_all_explitive_times
from censor import censor
import sys
sys.path.append("Models/data")
from data_creator import create_gan_data


"""
Module that blurs all explitives 
in an audio file given

Parameters
--------------------
string-- path to audio .mp3 or .wav file
string: path to lyrics .txt file

Output
---------------
clean file's name (Timestamp)
"""
def clean_audio(audio_file_path, lyrics_path):

    explitive_times = get_all_explitive_times(audio_file_path, lyrics_path)

    #create_gan_data(audio_file_path, explitive_times, file=False)
    #np.save("audio1_gan_X.npy", gan)
    #np.save("audio1_disc_X.npy", disc)

    clean_file = censor(audio_file_path, explitive_times)

    return clean_file
