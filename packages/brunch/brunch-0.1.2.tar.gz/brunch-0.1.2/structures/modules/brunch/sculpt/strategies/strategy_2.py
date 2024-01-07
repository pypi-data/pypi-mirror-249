

'''
from brunch.sculpt.strategies.strategy_2 import strategy_2
'''

def strategy_2 ():
	BYTES_PER_PLATE = 512 * 512;

	BYTES = b''

	LOOP = 1
	while (LOOP <= (BYTES_PER_PLATE / 8)):
		BYTES += b'\xFF\xEF\xFF\xDF\xFF\xCF\xFF\xBF'
		LOOP += 1
		
	return BYTES;