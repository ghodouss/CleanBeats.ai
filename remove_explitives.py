from run_gentle import run_gentle




def get_all_explitive_times(audio_file_path, transcript):

    explitives = set()
    explitives.add("fuck")
    explitives.add("shit")
    explitive_times = []
    
    gentle_output = run_gentle(audio_file_path, transcript)

    for word in gentle_output:
        if word.word in explitives:
            explitive_time = {"start":word.start, "end":word.end}
            explitive_times.append(explitive_time)
    
    return explitive_times

get_all_explitive_times("eminem_curse.mp3", "em_lyrics.txt")