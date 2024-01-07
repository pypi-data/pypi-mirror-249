




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
	
	from brunch.erase import erase
	from brunch.sculpt.strategies.strategy_1 import strategy_1
	from brunch.sculpt.strategies.strategy_2 import strategy_2
	
	erase ({
		"DRIVE PATH": drive_path,
		"last_byte": drive_bytes - 1,
		#"last_byte": (512 * 512) * 10000,
		
		"sculpt": {
			"strategies": [{
				"bytes per plate": 512 * 512,
				"BYTES": strategy_1 ()
			},{
				"bytes per plate": 512 * 512,
				"BYTES": strategy_2 ()
			}]
		},
		"scan": {
			"bytes per plate": 512 * 512
		}
	})
	
checks = {
	"ENTIRE DRIVE": CHECK_1	
}
