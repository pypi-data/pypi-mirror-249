

'''
from brunch.sculpt.strategies.strategies.1 import strategy_1
'''

from fractions import Fraction

def strategy_1 ():
	proceeds = b''

	eight_bytes = b'\x00\x01\x00\x02\x00\x03\x00\x04';

	'''
		512 = 8 * 8 * 8
		
		
		bytes_per_plate = 512 * 512 = 262144

		last_loop = 262144 / 8 = 32768
	'''
	bytes_per_plate = Fraction (512) * Fraction (512);
	last_loop = Fraction (bytes_per_plate, 8)

	

	'''
		>>> 32769 <= Fraction (262144 / 8)
		False
		>>> 32768 <= Fraction (262144 / 8)
		True
		>>> 32767 <= Fraction (262144 / 8)
		True
	'''
	loop = 1
	while (loop <= last_loop):
		proceeds += eight_bytes
		loop += 1
		
	return proceeds;