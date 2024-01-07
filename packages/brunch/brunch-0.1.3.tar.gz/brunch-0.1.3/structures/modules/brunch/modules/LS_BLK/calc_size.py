
'''
	#
	#	This raises an exception is the drive is not found.
	#

	drive_path = "/dev/sdb"

	import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
	drive_bytes = LS_BLK_calc_size.solidly (
		drive_path = drive_path
	)
'''

'''
	drive_path = "/dev/sdb"

	import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
	drive_bytes = LS_BLK_calc_size.solidly (
		drive_path = drive_path
	)
	
	import brunch.scan.is_last_byte as is_last_byte
	[ is_last, note ] = is_last_byte.deem ({
		"drive path": drive_path,
		"last_byte": drive_bytes + 1
	})
	if (is_last == False):
		raise Exception (note)
'''

'''
	lsblk -b -p --json

	{
	   "blockdevices": [
		  {
			 "name": "/dev/sdb",
			 "maj:min": "8:16",
			 "rm": true,
			 "size": 2032664576,
			 "ro": false,
			 "type": "disk",
			 "mountpoints": [
				 null
			 ]
		  }
	   ]
	}
'''

import json
import subprocess

def solidly (
	drive_path = ""
):
	assert (len (drive_path) >= 1), drive_path

	outlet = subprocess.run (
		["lsblk", "-b", "-p", "--json"], 
		capture_output = True
	)
	
	drive_bytes = ""
	found = False
	
	drives = json.loads (outlet.stdout.decode ("utf-8")) ['blockdevices']
	for drive in drives:
		if (drive ['name'] == drive_path):
			print ('drive:', drive)
			
			drive_bytes = drive ['size']
			found = True;
			break;
			
	if (not found):
		raise Exception (f"A drive with path '{ drive_path }' was not found.")
			
			
			
	return int (drive_bytes)