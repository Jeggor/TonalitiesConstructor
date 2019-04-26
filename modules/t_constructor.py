from functools import reduce
from sound import PITCHES, get_chord_freqs, get_full_scale_freqs
from wave_interface import create_scale_wav, create_chords_wav, play_wav, stop_wav

PLAY = False
WAV_SUBDIR = 'Tonalities\\'

def generate_line(lowest_pitch_index, length):
	return [PITCHES[(lowest_pitch_index + i * 7) % 12] for i in range(length)]
	

def generate_lattice(base_pitch, rows, columns):
	base_index = PITCHES.index(base_pitch)
	top_left_pitch_index = (base_index - 7 * (columns // 2) + 4 * (rows // 2)) % 12
		
	base_column = [PITCHES[(top_left_pitch_index - i * 4) % 12] for i in range(rows)]
	
	return [generate_line(PITCHES.index(base_column[i]), columns) for i in range(rows)]

	
def print_lattice(lattice):
	for i in range(len(lattice)):
		print(''.join(map(lambda c: '{0:<5}'.format(c), lattice[i])))
		print()
		
	print()

def first_quarter(base_index):
	return [PITCHES[base_index], PITCHES[(base_index + 4) % 12], PITCHES[(base_index + 7) % 12]]
	
	
def second_quarter(base_index):
	return [PITCHES[base_index], PITCHES[(base_index + 4) % 12], PITCHES[(base_index - 7) % 12]]
	
	
def third_quarter(base_index):
	return [PITCHES[base_index], PITCHES[(base_index + 7 - 4) % 12], PITCHES[(base_index + 7) % 12]]
	
	
def fourth_quarter(base_index):
	return [PITCHES[base_index], PITCHES[(base_index - 4) % 12], PITCHES[(base_index + 7) % 12]]
	
	
major = first_quarter
minor = third_quarter

	
def quarter_to_string(quarter):
	if quarter == first_quarter:
		return 'major(I)'
	if quarter == second_quarter:
		return 'II'
	if quarter == third_quarter:
		return 'minor(III)'
	if quarter == fourth_quarter:
		return 'IV'
	else:
		return 'Unknown'
	
def sort_scale(base_index, scale):
	sorted_scale = [PITCHES[base_index]]
	for i in range(len(PITCHES) - 1):
		if scale.__contains__(PITCHES[(base_index + 1 + i) % 12]):
			sorted_scale.append(PITCHES[(base_index + 1 + i) % 12])
			
	return sorted_scale
	
	
#mode - true = q, false = t
def construct_tonality(base, quarter_function, mode):
	if mode:
		return construct_q_tonality(base, quarter_function)
	else:
		return construct_t_tonality(base, quarter_function)
	
	
def construct_q_tonality(base, quarter_function):
	base_index = PITCHES.index(base)
	
	tonic = quarter_function(base_index)
	dominant = quarter_function((base_index + 7) % 12)
	subdominant = quarter_function((base_index - 7) % 12)
	
	scale = sort_scale(base_index, list(set(tonic + dominant + subdominant)))
	
	return {'T': tonic, 'S': subdominant, 'D': dominant, 'Scale': scale, 'Len': len(scale),
		'Name': '{0} - {1} ({2})'.format(base, quarter_to_string(quarter_function), 'perfect fifth')}

	
def construct_t_tonality(base, quarter_function):
	base_index = PITCHES.index(base)
	
	tonic = quarter_function(base_index)
	dominant = quarter_function((base_index + 4) % 12)
	subdominant = quarter_function((base_index - 4) % 12)
	
	scale = sort_scale(base_index, list(set(tonic + dominant + subdominant)))
	
	return {'T': tonic, 'S': subdominant, 'D': dominant, 'Scale': scale, 'Len': len(scale), 
		'Name': '{0} - {1} ({2})'.format(base, quarter_to_string(quarter_function), 'major third')}
	

def print_result(tonality):
	print('{0:>6} {1}'.format('Name:', tonality['Name']))
	print('{0:>6} {1}'.format('Scale:', reduce(lambda acc, s: acc + s, map(lambda note: '{0:<3}'.format(note), tonality['Scale']))))
	print('{0:>6} {1}'.format('T:', reduce(lambda acc, s: acc + s, map(lambda note: '{0:<3}'.format(note), tonality['T']))))
	print('{0:>6} {1}'.format('S:', reduce(lambda acc, s: acc + s, map(lambda note: '{0:<3}'.format(note), tonality['S']))))
	print('{0:>6} {1}'.format('D:', reduce(lambda acc, s: acc + s, map(lambda note: '{0:<3}'.format(note), tonality['D']))))
	print('{0:>6} {1}'.format('Len:', tonality['Len']))
	print()
	
	scale_freqs = get_full_scale_freqs(tonality['Scale'])
	full_cadence = [get_chord_freqs(tonality['T'], True),	
					get_chord_freqs(tonality['S'], True),
					get_chord_freqs(tonality['D'], True), 
					get_chord_freqs(tonality['T'], True)]
	
	scale_wav_name = WAV_SUBDIR + tonality['Name'] + ' scale.wav'
	full_cadence_wav_name = WAV_SUBDIR + tonality['Name'] + ' full_cadence.wav'
	
	create_scale_wav(scale_wav_name, scale_freqs)
	create_chords_wav(full_cadence_wav_name, full_cadence)
	
	if PLAY:
		print('Playing scale...')
		play_wav(scale_wav_name)
		input()
		print('Playing full cadance...')
		play_wav(full_cadence_wav_name)
		input()
		stop_wav()
	

if __name__ == '__main__':
	quaters = [first_quarter, second_quarter, third_quarter, fourth_quarter]
	modes = [True, False]
	
	for pitch in PITCHES:
		print_lattice(generate_lattice(pitch, 5, 5))
		for mode in modes:
			for quarter in quaters:
				print_result(construct_tonality(pitch, quarter, mode))