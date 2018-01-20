from remove_explitives import get_all_explitive_times
from censor import censor



def clean_audio(audio_file_path, lyrics):

    explitive_times = get_all_explitive_times(audio_file_path, lyrics)

    clean_file = censor(audio_file_path, explitive_times)

    return clean_file


clean_audio("eminem_curse.mp3", "em_lyrics.txt")