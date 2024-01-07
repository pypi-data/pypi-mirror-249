




import brunch.sculpt as sculpt
import brunch.scan as scan

import os
drive_path = os.environ.get ('drive_path')
drive_bytes = int (os.environ.get ('drive_bytes'))
#
#	   40 GB ~= 40,000,000,000
#	 	1 GB ~=  1,000,000,000
#	 1/10 GB ~=    100,000,000	
#
assert (drive_bytes >= 100000000)

'''
	xxd -len 100 /dev/sdc
	xxd -len 100 -seek 40018597788 /dev/sdc
'''
def CHECK_1 ():
	print ("STARTING CHECK")

	BYTES_PER_PLATE = 512 * 512;
	#BYTES_PER_PLATE = 512;

	BYTES_INDEXES = [
		0, 
		drive_bytes - 1 
	]
	
	'''
	BYTES_INDEXES = [
		0, 
		drive_bytes - 1 
	]
	'''
	
	#
	#	40018597888 % (512 * 512) = 219136
	#
	#LAST_BYTES_PER_PLATE = drive_bytes % (512 * 512)
	LAST_BYTES_PER_PLATE = (BYTES_INDEXES[1] - BYTES_INDEXES[0] + 1) % (512 * 512)
		
	print ("LAST_BYTES_PER_PLATE:", LAST_BYTES_PER_PLATE)	
	#return;
		
	def COOK ():
		BYTES = b''

		LOOP = 1
		while (LOOP <= (BYTES_PER_PLATE / 2)):
			BYTES += b'\x81\x33'
			LOOP += 1
			
		return BYTES;
		
	PLATE = COOK ()
	assert (len (PLATE) == BYTES_PER_PLATE)
	
	def scan_1 ():
		print ("STARTING scan")
		
		LOOP = 1
		def PROGRESS (PARAMS):
			#print (PARAMS)
		
			nonlocal LOOP;
			INDEXES = PARAMS ["INDEXES"]
			LAST_scan = PARAMS ["LAST scan"]

			if (LOOP == 1000 or LAST_scan):
				PERCENT = str (100 * (INDEXES [1] / drive_bytes))
				print (
					"scan:",
					INDEXES[0],
					INDEXES[1] - INDEXES[0], 
					"%:", PERCENT
				)
				
				LOOP = 1;
			
			LOOP += 1
			
			if (LAST_scan):
				assert (
					len (PARAMS["PLATE"]) ==
					LAST_BYTES_PER_PLATE
				)
				assert (
					PARAMS["PLATE"] == 
					PLATE [0:LAST_BYTES_PER_PLATE]
				)

			
			else:
				assert (
					len (PARAMS["PLATE"]) ==
					len (PLATE)
				)
				assert (
					PARAMS ["PLATE"] == 
					PLATE
				)


		scan.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": BYTES_INDEXES,		
			"bytes per plate": BYTES_PER_PLATE,
			
			"PROGRESS": PROGRESS
		})

		
	def sculpt_1 ():	
		print ("STARTING sculpt")
	
		LOOP = 1
		def PROGRESS (PARAMS):
			nonlocal LOOP;
			INDEXES = PARAMS ["INDEXES"]
			SIZE = PARAMS ["SIZE"]
			LAST_LOOP = PARAMS ["LAST_LOOP"]
	
			if (LOOP == 1000):
				PERCENT = str (100 * (INDEXES [1] / drive_bytes))
				print (
					INDEXES[0],
					INDEXES[1] - INDEXES[0], 
					"%:", PERCENT
				)
				
				LOOP = 1;
			
			LOOP += 1
			
			
			if (LAST_LOOP):
				assert (
					PARAMS["SIZE"] ==
					LAST_BYTES_PER_PLATE
				)
				
				print ("LAST sculpt LOOP CHECK IS DONE")
				
			else:
				assert (
					PARAMS["SIZE"] ==
					BYTES_PER_PLATE
				)

		sculpt.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": BYTES_INDEXES,		
			"BYTES FOR PLATE": PLATE,
			
			"PROGRESS": PROGRESS
		})
	

	#sculpt_1 ()
	#print ("sculpt FUNCTION RETURNED")
	
	scan_1 ()
	print ("scan FUNCTION RETURNED")
	

	
checks = {
	"ENTIRE DRIVE": CHECK_1	
}
