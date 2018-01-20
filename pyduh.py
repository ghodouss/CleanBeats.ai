from pydub import AudioSegment
from pydub.playback import play

# read in audio file and get the two mono tracks

def censor(file_name,snips=[{"start":20,"end":25},{"start":30,"end":35}]):

	sound_stereo = AudioSegment.from_file(filename, format="mp3")
	words=snips
	for i in words:
		s=i["start"]
		e=i["end"]
		samp=sound_stereo[float(s)*1000:float(e)*1000]
		sound_monoL = samp.split_to_mono()[0]
		sound_monoR = samp.split_to_mono()[1]
		# Invert phase of the Right audio file
		sound_monoR_inv = sound_monoR.invert_phase()
	
		# Merge two L and R_inv files, this cancels out the centers
		sound_CentersOut = sound_monoL.overlay(sound_monoR_inv)
		sound_stereo=sound_stereo[:float(s)*1000]+sound_CentersOut+sound_stereo[float(e)*1000:]


	# Export merged audio file
	fh = sound_stereo.export("output.mp3", format="mp3")

