




'''
	import brunch.scan as scan
'''

'''
	PARAMS = {
		"PLATE": PLATE,
		"BYTES INDEXES": [
			PLATE_INDEX_START,
			PLATE_INDEX_START + scan_SIZE
		]
	}
'''
def PROGRESS (PARAMS):
	return;


#
#	https://python-jsonschema.readthedocs.io/en/latest/
#
from jsonschema import validate
SCHEMA = {
    "type" : "object",
	"required": [ 
		"DRIVE PATH",
		"BYTES INDEXES", 
		"bytes per plate" 
	],
    "properties" : {
		"DRIVE PATH": {
			"type": "string"
		},
        "BYTES INDEXES" : { 
			"type" : "array",
		},
        "bytes per plate" : {
			"type" : "number"
		}
    }
}

def START (CARGO):
	#print ("CARGO", CARGO)

	validate (
		instance = CARGO, 
		schema = SCHEMA
	)

	DRIVE_PATH = CARGO ["DRIVE PATH"]
	BYTES_PER_PLATE = CARGO ["bytes per plate"]
	BYTES_INDEXES = CARGO ["BYTES INDEXES"]
	
	#print ("VALID?")
	
	
	if ("PROGRESS" in CARGO):
		PROGRESS = CARGO ["PROGRESS"]
	
	
	#
	#	--
	#

	'''
		bytes per plate: 10
		BYTE INDEXES: [ 0, 28 ]
	
		 0 TO  9
		10 TO 19
		
		20 TO 29
	'''

	MEAL_INDEX_START = BYTES_INDEXES [0];
	MEAL_INDEX_END = BYTES_INDEXES [1];

	with open (DRIVE_PATH, "rb") as f:
		f.seek (MEAL_INDEX_START)
		#PLATE_INDEX_0 = f.tell ()
		
		print (f"opened drive '{ DRIVE_PATH }' for scanning")
		
		LAST_scan = False
		PLATE = True;
		while PLATE:
			PLATE_INDEX_START = f.tell ()
					
			#print (PLATE_INDEX_START, BYTES_PER_PLATE, MEAL_INDEX_END)
					
			#
			#	CHECK IF A FULL PLATE WOULD 
			#	PUT THE scanNER PAST THE LAST INDEX
			#
			if (
				(PLATE_INDEX_START + BYTES_PER_PLATE) > MEAL_INDEX_END
			):
				LAST_scan = True
				scan_SIZE = MEAL_INDEX_END - PLATE_INDEX_START + 1

				#print ("PAST LAST INDEX, scan_SIZE =", scan_SIZE)

				if (scan_SIZE <= 0):
					return;
				
			else:
				scan_SIZE = BYTES_PER_PLATE;
				
			#print ("scan SIZE:", scan_SIZE)
			
			PLATE = f.read (scan_SIZE)
			if (len (PLATE) == 0):
				print ("THERE WERE NO BYTES LEFT TO scan")
				return;	
			
			#print ("TELL:", f.tell ())
			
			PLATE_INDEX_END = f.tell () - 1
			
			PROGRESS ({
				"PLATE": PLATE,
				"scan SIZE": scan_SIZE,
				"LAST scan": LAST_scan,
				"INDEXES": [
					PLATE_INDEX_START,
					PLATE_INDEX_END
				]
			})	
			
			if (LAST_scan):
				print ()
				print ("scan IS DONE")
				print ()
				
				f.close ()
				
				return;
			
			
	
			 
		 
