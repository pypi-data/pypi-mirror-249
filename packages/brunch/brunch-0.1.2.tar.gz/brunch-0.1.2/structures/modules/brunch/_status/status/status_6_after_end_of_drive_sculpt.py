
'''
	WHERE DRIVE BYTE COUNT = 40018597888

	xxd -len 100 -seek 40018597788 /dev/sdb
			
	#
	#	THIS SHOULD READ ONE BYTE
	#
	xxd -len 100 -seek 40018597887 /dev/sdb
'''

'''
	blockdev --getsz /dev/sdb
'''

import brunch.scan.can_scan as can_scan
import brunch.sculpt as sculpt	
	
import os
drive_path = os.environ.get ('drive_path')	

import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
drive_bytes = LS_BLK_calc_size.solidly (
	drive_path = "/dev/sdb"
)


def CHECK_1 ():	
	

	def PROGRESS (PARAMS):
		#nonlocal BYTE_STRING;	
		#BYTE_STRING += PARAMS ['PLATE']

		return;

	try:
		sculpt.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": [ 
				drive_bytes,
				drive_bytes
			],		
			"BYTES FOR PLATE": b'\x00',
			
			"PROGRESS": PROGRESS
		})
	except Exception as E:
		print (E)
		
		assert (str (E) == "[Errno 28] No space left on device")
	
checks = {
	"CHECK 1": CHECK_1
}