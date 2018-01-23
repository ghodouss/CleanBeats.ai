from pydub import AudioSegment
from canetis.align import align

def segs_to_gentle(segments):
    """
    Converts output of align
    to a standard gentle output

    Parameters
    -----------------------
    list of Segment Object

    Output
    ------------------
    list of Gentle Word Objects
    """
    gentle_output = []

    for seg in segments:
        gentle_output += seg.gentle

    return gentle_output


def get_explitives(gentle_output):
    explitives = ["shit", "fuck", "damn", "dick"]
    explitive_times = []

    for word in gentle_output:
        for explitive in explitives:
            if explitive in word.word and word.success():
                explitive_time = {"word":word.word, "start":word.start, "end":word.end}
                explitive_times.append(explitive_time)
    print(explitive_times)

    return explitive_times
    

def get_all_explitive_times(audio_file_path, text_file_path):

    """
    Module that finds the timestamps
    of every explitive in an audio file

    Inputs
    ----------------------
    String Path to .wav or .mp3 file
    String Path to .txt transcript file

    Outputs
    --------------------
    List of timestamp dicts
    """
    
    # run forced alignment on file
    segments = align(audio_file_path, text_file_path)
    gentle_output = segs_to_gentle(segments)

    # get list of explitive times
    explitive_times = get_explitives(gentle_output)
    
    #return explitive times
    return explitive_times



    






