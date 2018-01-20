from pydub import AudioSegment
from pydub.playback import play
import time
import os
from gtts import gTTS
# read in audio file and get the two mono tracks
'''
This function takes the file name of the song and the portions to be censored as a list and then removes the vocals from the required bits

Input:
file_name: The name of the song file
snips: Dictionary of sections to be removed

Output: censored file

'''
def create_gan_data(file_name,snips=[{"start":20,"end":25,"word":"hello"},{"start":30,"end":35,"word":"bye"}]):

    name = str(time.time()) + ".mp3"

    sound_stereo = AudioSegment.from_file(file_name, format="mp3")
    sound_real=sound_stereo
    #os.remove(file_name)

    words=snips
    for i in words:
        start = int(max(i["start"]-.1, 0)*1000)
        end = int(min((i["end"]+.1)*1000, len(sound_stereo)-1))
        samp=sound_stereo[start: end]
        sound_monoL = samp.split_to_mono()[0]
        sound_monoR = samp.split_to_mono()[1]
        # Invert phase of the Right audio file
        sound_monoR_inv = sound_monoR.invert_phase()
    
        # Merge two L and R_inv files, this cancels out the centers
        sound_CentersOut = sound_monoL.overlay(sound_monoR_inv)
        sound_stereo = sound_stereo[:start]+sound_CentersOut+sound_stereo[end:]
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
        sound_stereo=sound_stereo.overlay(repl,gain_during_overlay=12,position=start)
        if (((start+end)/2)>1500 and ((start+end)/2)<(len(sound_stereo)-1500)):
            clip=sound_stereo[((start+end)/2)-1500:((start+end)/2)+1500]
            clip.export("temp.mp3",format="mp3")
            clipr=sound_real[((start+end)/2)-1500:((start+end)/2)+1500]
            clipr.export("realtemp.mp3",format="mp3")
        ######################
        #ADD LIBROSA HERE
        #
        #
        #
        #######################

        os.remove("temp.mp3")

    # Export merged audio file
    fh = sound_stereo.export("clean_files/"+name, format="mp3")

    return name

if __name__ == '__main__':
    create_gan_data("sample.mp3",snips=[{"start":20,"end":22,"word":"hello"},{"start":30,"end":32,"word":"bye"}])


