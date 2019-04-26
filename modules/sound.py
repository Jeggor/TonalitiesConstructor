from winsound import Beep

#До первой октавы (C4 в научной нотации)
C4_FREQ = 440 * 2 ** (-9 / 12)
C0_FREQ = C4_FREQ / 16

DEFAULT_DURATION = 250

ALL_PITCHES = {}

PITCH_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

class Durations:
	def __init__(self, bpm):
		if bpm == 0:
			self.bpm = 120
		else:
			self.bpm = 120
		
		self.quarter = 60000 // self.bpm
		
		self.half = 2 * self.quarter
		self.whole = 2 * self.half
		
		self.eighth = self.quarter // 2
		self.sixteenth = self.eighth // 2


INTERVALS = {'P1': 0, 'm2': 1, 'M2': 2, 'm3': 3, 'M3': 4, 'P4': 5, 'A4': 6, 'D5': 6, 'P5': 7,
				'm6': 8, 'M6': 9, 'm7': 10, 'M7': 11, 'P8': 12}

HALFSTEPS_PER_OCTAVE = 12
	
PITCHES = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
			
FREQ_MAP = { }


def change_freq(halfsteps, base_freq = C4_FREQ):
	return base_freq * 2 ** (halfsteps / HALFSTEPS_PER_OCTAVE)


def get_halfsteps_count(base_pitch, next_pitch):
	base_pitch_index = PITCHES.index(base_pitch)
	next_pitch_index = PITCHES.index(next_pitch)
	
	return (next_pitch_index - base_pitch_index) % HALFSTEPS_PER_OCTAVE
				
			
def get_up_scale_freqs(scale):
	base_pitch = scale[0]
	base_pitch_freq = FREQ_MAP[base_pitch]
	
	freq_list = []
	for i, pitch in enumerate(scale):
		halfsteps_count = get_halfsteps_count(base_pitch, pitch)
		freq_list.append(change_freq(halfsteps_count, base_pitch_freq))
	
	freq_list.append(change_freq(INTERVALS['P8'], base_pitch_freq))
	
	return freq_list


def get_down_scale_freqs(scale):
	return get_up_scale_freqs(scale)[::-1]


def get_full_scale_freqs(scale):
	return get_up_scale_freqs(scale) + get_down_scale_freqs(scale)[1::]


def get_chord_freqs(chord, double = False):
	base_pitch = chord[0]
	base_pitch_freq = FREQ_MAP[base_pitch]
	
	freq_list = []
	for i, pitch in enumerate(chord):
		halfsteps_count = get_halfsteps_count(base_pitch, pitch)
		freq_list.append(change_freq(halfsteps_count, base_pitch_freq))
		
	if double:
		freq_list.append(change_freq(INTERVALS['P8'], base_pitch_freq))
		
	return freq_list

def play_pitch(pitch_freq, duration = DEFAULT_DURATION):
	Beep(int(pitch_freq), duration)
	
# Pitches - list of tuples
# Tuple may contain wether single pitch name and duration of pitch (in seconds), e.g. ('C4', 0.5)
# or list of simultaneously played pitches (for chord), e.g. (['C4', 'E4', 'G4'], 0.5)
# All alterated pitches names must be with sharps (#)
def pitches_to_freqs(pitches):
	pitches_list = []
	for i, value in enumerate(pitches):
		if value[0].__class__.__name__ == 'list':
			chord_list = []
			for j, pitch in enumerate(value[0]):
				chord_list.append(ALL_PITCHES.get(str.upper(pitch), 0))
				
			pitches_list.append((chord_list, value[1]))
			
		if value[0].__class__.__name__ == 'str':
			pitches_list.append((ALL_PITCHES.get(str.upper(value[0]), 0), value[1]))
			
	return pitches_list


def transpose(freqs, halfsteps):
	if halfsteps == 0:
		return freqs
		
	transposed = []
	for i, value in enumerate(freqs):
		if value[0].__class__.__name__ == 'list':
			chord = []
			for j, chord_pitch in enumerate(value[0]):
				chord.append(change_freq(halfsteps, chord_pitch))
				
			transposed.append((chord, value[1]))
		else:	
			transposed.append((change_freq(halfsteps, value[0]), value[1]))
	
	return transposed

#def play_scale(scale, duration = DEFAULT_DURATION):
	#print('Up')
	#for pitch_freq in get_up_scale_freqs(scale):
	#	play_pitch(pitch_freq, duration)
		
	#print('Down')
	#for pitch_freq in get_down_scale_freqs(scale):
	#	play_pitch(pitch_freq, duration)
		
	#print('Full')
	#for pitch_freq in get_full_scale_freqs(scale):
	#	play_pitch(pitch_freq, duration)
	
for i, pitch in enumerate(PITCHES):
	FREQ_MAP[pitch] = change_freq(i) 
	
for octave in range(10):
	for i, pitch_name in enumerate(PITCH_NAMES):
		ALL_PITCHES[pitch_name + str(octave)] = change_freq(12 * octave + i, C0_FREQ)