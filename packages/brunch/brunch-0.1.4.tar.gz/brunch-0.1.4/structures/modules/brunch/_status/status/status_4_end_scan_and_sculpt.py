




import brunch.sculpt as sculpt
import brunch.scan as scan

import os
drive_path = os.environ.get ('drive_path')


import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
drive_bytes = LS_BLK_calc_size.solidly (
	drive_path = "/dev/sdb"
)

'''
	
'''
def CHECK_1 ():
	BYTE_COUNT = 29

	BYTES_INDEXES = [
		#
		#	BYTE 29, COUNTING BACKWARDS FROM THE LAST BYTE OF THE DRIVE
		#
		drive_bytes - 1 - (BYTE_COUNT - 1), 
		
		#
		#	THE LAST BYTE OF THE DRIVE
		#
		drive_bytes - 1 
	]
	
	'''
		0  3  6  9  c  f  2
	     12 45 78 ab de 01
	'''
	PLATE = b'\x00\x03\x06\x09\x0c\x0f\x12\x15\x18\x1a'

	def scan_1 ():
		BYTE_STRING = b""
		def PROGRESS (PARAMS):
			nonlocal BYTE_STRING;
			BYTE_STRING += PARAMS ['PLATE']		

		scan.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": BYTES_INDEXES,		
			"bytes per plate": 10,
			
			"PROGRESS": PROGRESS
		})

		print ("scanNED:", BYTE_STRING)		
		print (len (BYTE_STRING))		
		assert (len (BYTE_STRING) == BYTE_COUNT)
		assert (
			BYTE_STRING == 
			b"".join ([
				PLATE,
				PLATE,
				PLATE[0:9]
			])
		)
		
		
	def sculpt_1 ():					
		def PROGRESS (PARAMS):
			#nonlocal BYTE_STRING;	
			#BYTE_STRING += PARAMS ['PLATE']

			return;

		sculpt.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": BYTES_INDEXES,		
			"BYTES FOR PLATE": PLATE,
			
			"PROGRESS": PROGRESS
		})
	
		return;

	sculpt_1 ()
	scan_1 ()
	

	
checks = {
	"CHECK 1": CHECK_1	
}