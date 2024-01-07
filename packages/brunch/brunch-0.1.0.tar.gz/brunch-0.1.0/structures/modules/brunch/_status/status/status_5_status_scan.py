
'''
	
'''

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
	
import os
drive_path = os.environ.get ('drive_path')	


import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
drive_bytes = LS_BLK_calc_size.solidly (
	drive_path = "/dev/sdb"
)

def CHECK_1 ():	
	[ scanNED, PLATE ] = can_scan.START ({
		"DRIVE PATH": drive_path,
		
		#
		#	1 AFTER THE LAST INDEX OF BYTES ON THE DEVICE
		#
		"BYTE INDEX": drive_bytes
	})
	
	print ("PLATE:", PLATE)
	
	assert (scanNED == False)
	
checks = {
	"CHECK 1": CHECK_1
}