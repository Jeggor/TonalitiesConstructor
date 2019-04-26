import numpy as np

from scipy.io import wavfile
from scipy import interpolate

from operator import itemgetter

import pygame

import sound

pygame.init()

SAMPLE_RATE = 44100

DEFAULT_DURATION = 0.5

DEFAULT_AMPLITUDE = 1000.0
MAX_AMPLITUDE = DEFAULT_AMPLITUDE * 2

AMPLITUDE_VALUES = {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0: 0.0}

DEFAULT_TIMBRE = [1.0, 0.3, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

import os

FILE_PATH = os.path.dirname(__file__) + '\\Wav files\\'

def get_sine_wave(freq, duration = DEFAULT_DURATION):
	array_length = duration * SAMPLE_RATE
	factor = freq * 2 * np.pi / SAMPLE_RATE
	return np.sin(np.arange(array_length, dtype = np.int16) * factor)


def get_harmonics(freq, duration = DEFAULT_DURATION, timbre = DEFAULT_TIMBRE):
	harmonics = []
	for i, harm_ampl in enumerate(timbre):
		harmonics.append(DEFAULT_AMPLITUDE * harm_ampl * get_sine_wave(freq * (i + 1), duration))
	
	return sum(harmonics)


def get_sound(freq, duration = DEFAULT_DURATION, timbre = DEFAULT_TIMBRE):
	sine_wave = get_harmonics(freq, duration, timbre)

	interp = interpolate.interp1d([*AMPLITUDE_VALUES.keys()], [*AMPLITUDE_VALUES.values()], kind = 'slinear')
	factor = 1.0 / len(sine_wave)
	shape = interp(np.arange(len(sine_wave)) * factor)
    
	return np.array(sine_wave * shape, dtype = np.int16)


def create_scale_wav(file_name, scale_freqs):
	sounds = []
	for i, pitch_freq in enumerate(scale_freqs):
		sounds.append(get_sound(pitch_freq))
		
	data = np.concatenate(sounds)
	wavfile.write(FILE_PATH + file_name, SAMPLE_RATE, data)


def calc_chord_wave(chord, duration = DEFAULT_DURATION):
	chord_pitches = []
	for j, chord_pitch in enumerate(chord):
		chord_pitches.append(get_sound(chord_pitch, duration))	
	
	return sum(chord_pitches)

def create_chords_wav(file_name, chords_freqs):
	sounds = []
	for i, chord in enumerate(chords_freqs):
		sounds.append(calc_chord_wave(chord, DEFAULT_DURATION * 2))
		
	data = np.concatenate(sounds)
	wavfile.write(FILE_PATH + file_name, SAMPLE_RATE, data)

# pitch_freqs is list of tuples
# Tuple definition may be seen in sound.pitches_to_freqs function description
def create_arbitrary_wav(file_name, pitch_freqs):
	sounds = []
	for i, value in enumerate(pitch_freqs):
		if value[0].__class__.__name__ == 'list':
			sounds.append(calc_chord_wave(value[0], value[1]))
		else:	
			sounds.append(get_sound(value[0], value[1]))
	
	data = np.concatenate(sounds)
	wavfile.write(FILE_PATH + file_name, SAMPLE_RATE, data)


def play_wav(file_name):
	pygame.mixer.music.load(FILE_PATH + file_name)
	pygame.mixer.music.play()

def stop_wav():
	pygame.mixer.music.stop()

def test():
	melody = [('C4', 1), ('D#4', 0.5), ('F4', 0.5), ('C4', 1.0),
				('G#3', 0.5), ('A#3', 0.5), ('C4', 1.0), 
				('D#4', 0.5), ('F4', 0.5), ('D4', 1.0),
				(['D4', 'F4', 'A4', 'C5'], 0.5), #SII7
				(['D4', 'F4', 'G4', 'B4'], 0.5), #D43
				(['D#4', 'G4', 'C5'], 1.0) #T6
				]
				
	melody_freqs = sound.pitches_to_freqs(melody)
	create_arbitrary_wav('Test.wav', melody_freqs)
	
	play_wav('Test.wav')

#if __name__ == '__main__':
	#test()