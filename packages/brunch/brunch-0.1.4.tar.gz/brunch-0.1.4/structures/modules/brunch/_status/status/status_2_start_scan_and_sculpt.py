




import brunch.sculpt as sculpt
import brunch.scan as scan

import os
drive_path = os.environ.get ('drive_path')

'''
	checks THAT 29 BYTES CAN BE WRITTEN
	AND READ, STARTING AT DRIVE INDEX 0.
'''
def CHECK_1 ():
	'''
		0, 2, 4, 6, 8, A, C, E
		1, 3, 5, 7, 9, B, D, F
	'''
	PLATE = b'\x00\x02\x04\x06\x08\x0a\x0c\x0e\x10\x12'

	def scan_1 ():
		BYTE_STRING = b""

		COUNT = 1
		def PROGRESS (PARAMS):
			nonlocal BYTE_STRING;
			nonlocal COUNT;
						
			if (COUNT <= 2):
				assert (PARAMS ['PLATE'] == PLATE)
			else:
				assert (PARAMS ['PLATE'] == PLATE[0:9])
		
			BYTE_STRING += PARAMS ['PLATE']

			COUNT += 1
		
			return;

		scan.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": [ 0, 28 ],		
			"bytes per plate": 10,
			
			"PROGRESS": PROGRESS
		})
		
		
		assert (len (BYTE_STRING) == 29)
		print (BYTE_STRING)
		
	def sculpt_1 ():
		

		
		def PROGRESS (PARAMS):
			#nonlocal BYTE_STRING;	
			#BYTE_STRING += PARAMS ['PLATE']

			return;

		sculpt.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": [ 0, 28 ],		
			"BYTES FOR PLATE": PLATE,
			
			"PROGRESS": PROGRESS
		})
		
		return;
	
	sculpt_1 ()
	scan_1 ()

	return;
	
	
checks = {
	"CHECK 1": CHECK_1
}