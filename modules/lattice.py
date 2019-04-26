from functools import reduce
from sound import pitches
	
def generate_line(lowest_pitch_index, length):
	return [pitches[(lowest_pitch_index + i * 7) % 12] for i in range(length)]
	

def generate_lattice(base_pitch, rows, columns):
	base_index = pitches.index(base_pitch)
	top_left_pitch_index = (base_index - 7 * (columns // 2) + 4 * (rows // 2)) % 12
		
	base_column = [pitches[(top_left_pitch_index - i * 4) % 12] for i in range(rows)]
	
	return [generate_line(pitches.index(base_column[i]), columns) for i in range(rows)]

	
def print_lattice(lattice):
	for i in range(len(lattice)):
		print(''.join(map(lambda c: '{0:<5}'.format(c), lattice[i])))
		print()
	print()