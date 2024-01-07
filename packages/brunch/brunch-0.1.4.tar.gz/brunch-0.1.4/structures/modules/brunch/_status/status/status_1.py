




import brunch.scan as scan

def CHECK_1 ():
	import os
	drive_path = os.environ.get ('drive_path')
	print ("drive_path:", drive_path)

	BYTE_STRING = b""

	def PROGRESS (PARAMS):
		nonlocal BYTE_STRING;
		print (PARAMS)
	
		BYTE_STRING += PARAMS ['PLATE']
	
		return;

	scan.START ({
		"DRIVE PATH": drive_path,
		
		"BYTES INDEXES": [ 0, 28 ],		
		"bytes per plate": 10,
		
		"PROGRESS": PROGRESS
	})
	
	
	assert (len (BYTE_STRING) == 29)
	print (BYTE_STRING)

	return;
	
	
checks = {
	"CHECK 1": CHECK_1
}