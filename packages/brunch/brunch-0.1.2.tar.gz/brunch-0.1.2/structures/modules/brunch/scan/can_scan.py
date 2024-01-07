
'''
	import brunch.scan.can_scan as can_scan
	
	
	[ scanNED, PLATE ] = can_scan.START ({
		"DRIVE PATH": "/dev/sdb",
		
		"BYTE INDEX": 40018597888
	})
'''

def START (CARGO):	
	scan_SIZE = 512 * 512;
	BYTE_INDEX = CARGO ["BYTE INDEX"];
	DRIVE_PATH = CARGO ["DRIVE PATH"];

	print ("BYTE INDEX", BYTE_INDEX)
	print ("BYTE INDEX", type (BYTE_INDEX))

	with open (DRIVE_PATH, "rb") as f:
		f.seek (BYTE_INDEX)
		
		print ("TELL", f.tell ())
		PLATE = f.read (scan_SIZE)
		
		print ("TELL", f.tell ())
		
		if (len (PLATE) == 0):
			print ("THERE WERE NO BYTES LEFT TO scan")
			return [ False, PLATE ]

		return [ True, PLATE ]

	return [ "?", PLATE ]