




import brunch.sculpt as sculpt
import brunch.scan as scan

import os
drive_path = os.environ.get ('drive_path')

print ("drive_path:", drive_path)

import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
drive_bytes = LS_BLK_calc_size.solidly (
	drive_path = "/dev/sdb"
)

'''
	
'''
def check_1 ():
	byte_string = b""
	def PROGRESS (PARAMS):
		nonlocal byte_string;
		byte_string += PARAMS ['PLATE']		

	scan.START ({
		"DRIVE PATH": drive_path,
		
		"BYTES INDEXES": [ 
			drive_bytes - 1 - 1, 
			drive_bytes - 1 
		],		
		"bytes per plate": 10,
		
		"PROGRESS": PROGRESS
	})
	
	print ("VOW 3 - check 1:", len (byte_string))		
	assert (len (byte_string) == 2)



def check_2 ():
	byte_string = b""
	def PROGRESS (PARAMS):
		nonlocal byte_string;
		byte_string += PARAMS ['PLATE']		
		
		print (PARAMS)
	

	scan.START ({
		"DRIVE PATH": drive_path,
		
		"BYTES INDEXES": [ 
			drive_bytes - 1, 
			drive_bytes - 1 + 100000000000000
		],		
		"bytes per plate": 10,
		
		"PROGRESS": PROGRESS
	})
	
	print ("VOW 3 - check 2:", byte_string)	
	print ("VOW 3 - check 2:", len (byte_string))
	
	assert (len (byte_string) == 1), byte_string
		
def check_3 ():
	byte_string = b""
	def PROGRESS (PARAMS):
		nonlocal byte_string;
		byte_string += PARAMS ['PLATE']		
	

	scan.START ({
		"DRIVE PATH": drive_path,
		
		"BYTES INDEXES": [ 
			drive_bytes - 1 + 1, 
			drive_bytes - 1 + 3
		],		
		"bytes per plate": 10,
		
		"PROGRESS": PROGRESS
	})
	
	print ("VOW 3 - check 3:", byte_string)		
	assert (len (byte_string) == 0), byte_string

	
	
checks = {
	"A scan of the last 2 bytes with indexes [ last - 1, last ]": check_1,
	"A scan of the last byte, with indexes [ last, last + 3 ]": check_2,
	"A scan of zero bytes with indexes: [ last + 1, last + 3 ]": check_3	
}