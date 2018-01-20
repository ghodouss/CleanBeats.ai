import gentle

def run_gentle(audio_file_path, transcript):
    """
    Takes in a segment
    1. create new text file containing text
    2. create new audio with pydub
    3. run Gentle with these two
    4. delete text file/audio files

    Parameters
    ---------
    audio_file_path: filepath
    transript : string holding the relevant transcript for this segment
    """

    # run Gentle
    resources = gentle.Resources()
    with gentle.resampled(audio_file_path) as wavfile:
        aligner = gentle.ForcedAligner(resources, transcript)
        result = aligner.transcribe(wavfile).words

    return result
