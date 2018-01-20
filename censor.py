from pydub import AudioSegment
from pydub.playback import play
import time

# read in audio file and get the two mono tracks
'''
This function takes the file name of the song and the portions to be censored as a list and then removes the vocals from the required bits

Input:
file_name: The name of the song file
snips: Dictionary of sections to be removed

Output: censored file

'''
def censor(file_name,snips=[{"start":20,"end":25},{"start":30,"end":35}]):

	name = str(time.time()) + ".mp3"

	sound_stereo = AudioSegment.from_file(file_name, format="mp3")
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


	# Export merged audio file
	fh = sound_stereo.export(name, format="wav")

	return name


