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

    #build set of explitives to check
    explitives = set()
    explitives.add("fuck")
    explitives.add("shit")
    explitives.add("I'm")

    #store explitive time dicts
    explitive_times = []
    
    # run forced alignment on file
    segments = align(audio_file_path, text_file_path)
    gentle_output = segs_to_gentle(segments)

    # get list of explitive times
    for word in gentle_output:
        if word.word in explitives and word.success():
            explitive_time = {"word":word.word, "start":word.start, "end":word.end}
            explitive_times.append(explitive_time)
    
    #return explitive times
    return explitive_times



    






