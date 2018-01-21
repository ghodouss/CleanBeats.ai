from pydub import AudioSegment
from pydub.playback import play
import time
import os
from gtts import gTTS
import librosa
import numpy as np
import json
# read in audio file and get the two mono tracks
'''
This function takes the file name of the song and the portions to be censored as a list and then removes the vocals from the required bits

Input:
file_name: The name of the song file
snips: Dictionary of sections to be removed

Output: censored file

'''
def create_gan_data(audio_file_name, transcript_file_name):

    with open(transcript_file_name, "r") as f:
        content = f.read()
        words = json.loads(content)
    

    name = str(time.time()) + ".mp3"

    sound_stereo = AudioSegment.from_file(audio_file_name, format="mp3")
    sound_real=sound_stereo
    #os.remove(file_name)

    gan_data = []
    disc_truth = []

    for i in words:
        start = int(max(i["start"]-.1, 0)*1000)
        end = int(min((i["end"]+.1)*1000, len(sound_stereo)-1))
        if end-start<5:
            break
        samp=sound_stereo[start: end]
        sound_monoL = samp.split_to_mono()[0]
        sound_monoR = samp.split_to_mono()[1]
        # Invert phase of the Right audio file
        sound_monoR_inv = sound_monoR.invert_phase()
    
        # Merge two L and R_inv files, this cancels out the centers
        sound_CentersOut = sound_monoL.overlay(sound_monoR_inv)
        sound_stereo = sound_real[:start]+sound_CentersOut+sound_real[end:]
        tts = gTTS(text=i["word"], lang='en')
        tts.save("temp.mp3")
        repl=AudioSegment.from_file("temp.mp3", format="mp3")
        if len(repl)>len(sound_CentersOut):
            x=repl.frame_rate
            repl = repl._spawn(repl.raw_data, overrides={"frame_rate": int(repl.frame_rate *len(repl)/len(sound_CentersOut))})
            repl.set_frame_rate(x)

        else:
            sil=AudioSegment.silent(duration=int((len(sound_CentersOut)-len(repl))/2))
            repl=sil+repl+sil

        sound_stereo=sound_stereo.overlay(repl,gain_during_overlay=3,position=((start))) #+end)-len(repl))/2)
        if (((start+end)/2)>1500 and ((start+end)/2)<(len(sound_stereo)-1500)):
            clip=sound_stereo[((start+end)/2)-1500:((start+end)/2)+1500]
            clip.export("temp.wav",format="wav")
            clipr=sound_real[((start+end)/2)-1500:((start+end)/2)+1500]
            clipr.export("realtemp.wav",format="wav")

            gan_data.append(librosa.load("temp.wav")[0])
            disc_truth.append(librosa.load("realtemp.wav")[0])

    #os.remove("temp.wav")
    #os.remove("realtemp.wav")
    #os.remove("temp.mp3")

    gan_data = np.array(gan_data)
    disc_truth = np.array(disc_truth)
    return gan_data, disc_truth


if __name__ == "__main__":
 
    gan, disc = create_gan_data("audio3.mp3", "audio3.txt")

    np.save("audio4_gan_X.npy", gan)
    np.save("audio4_disc_X.npy", disc)


