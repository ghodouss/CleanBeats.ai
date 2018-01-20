from canetis.align import align


def segs_to_gentle(segments):
    gentle_output = []

    for seg in segments:
        gentle_output += seg.gentle_output

    return gentle_output




def get_all_explitive_times(audio_file_path, text_file_path):

    explitives = set()
    explitives.add("fuck")
    explitives.add("shit")
    explitive_times = []


    
    segments = align(audio_file_path, text_file_path)
    gentle_output = segs_to_gentle(segments)

    print(gentle_output)

    for word in gentle_output:
        if word.word in explitives:
            explitive_time = {"word":word.word, "start":word.start, "end":word.end}
            explitive_times.append(explitive_time)
    
    return explitive_times


print(get_all_explitive_times("eminem_curse.mp3", "em_lyrics.txt"))




