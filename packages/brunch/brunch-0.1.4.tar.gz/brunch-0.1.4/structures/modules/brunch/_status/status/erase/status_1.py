


'''
	env drive_path=/dev/sd_ python3 status.proc.py '_status/status/erase/status_1.py'
'''




import brunch.scan as scan

def check_1 ():
	import os
	drive_path = os.environ.get ('drive_path')
	print ("drive_path:", drive_path)

	from brunch.erase import erase
	from brunch.sculpt.strategies.strategy_1 import strategy_1
	from brunch.sculpt.strategies.strategy_2 import strategy_2
	
	last_byte = 100
	
	erase ({
		"skip over": 0,
		
		"DRIVE PATH": drive_path,
		"last_byte": last_byte,
		
		"sculpt": {
			"strategies": [{
				"BYTES": strategy_1 ()
			},{
				"BYTES": strategy_2 ()
			}]
		},
		"scan": {
			"bytes per plate": 512 * 512
		}
	})

	
	
checks = {
	"check 1": check_1
}