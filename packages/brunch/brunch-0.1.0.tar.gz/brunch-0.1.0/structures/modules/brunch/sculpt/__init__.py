
'''
import brunch.sculpt as sculpt

sculpt.START ({
	"DRIVE PATH": drive_path,
	
	"BYTES INDEXES": [ 0, 28 ],		
	"BYTES FOR PLATE": b'\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6',
	
	"PROGRESS": PROGRESS
})
'''


def PROGRESS (PARAMS):
	return;



def START (cargo):
	#
	#	https://python-jsonschema.readthedocs.io/en/latest/
	#
	from jsonschema import validate
	validate (
		instance = cargo, 
		schema = {
			"type" : "object",
			"required": [ 
				"DRIVE PATH",
				"BYTES INDEXES", 
				"BYTES FOR PLATE" 
			],
			"properties" : {
				"DRIVE PATH": {
					"type": "string"
				},
				
				"BYTES INDEXES" : { 
					"type" : "array",
				}
			}
		}
	)

	drive_path = cargo ["DRIVE PATH"]
	
	byte_for_plate = cargo ["BYTES FOR PLATE"]
	assert (type (byte_for_plate) == bytes)
	assert (len (byte_for_plate) >= 1)
	
	BYTES_PER_PLATE = len (byte_for_plate)
	BYTES_INDEXES = cargo ["BYTES INDEXES"]
	
	MEAL_INDEX_START = BYTES_INDEXES [0];
	MEAL_INDEX_END = BYTES_INDEXES [1];

	if ("PROGRESS" in cargo):
		PROGRESS = cargo ["PROGRESS"]

	with open (drive_path, "wb") as selector:
		selector.seek (MEAL_INDEX_START)
		
		print (f"OPENED DRIVE '{ drive_path }' FOR sculpting")
		
		#LOOP = 1
		LAST_LOOP = False;
		PLATE = True;
		while PLATE:
			#if (LOOP % 1000 == 0):
			#	print ("sculpting")
			#LOOP += 1
		
			PLATE_INDEX_START = selector.tell ()
			
			#print ("PLATE INDEX START:", PLATE_INDEX_START)
			
			#
			#	CHECK IF A FULL PLATE WOULD 
			#	PUT THE scanNER PAST THE LAST INDEX
			#
			if (
				(PLATE_INDEX_START + BYTES_PER_PLATE) > MEAL_INDEX_END
			):
				sculpt_SIZE = MEAL_INDEX_END - PLATE_INDEX_START + 1
				
				LAST_LOOP = True
				
				if (sculpt_SIZE <= 0):
					print ("sculpt ENDED, sculpt SIZE IS 0")
				
					return;
					
				sculpture = byte_for_plate [0:sculpt_SIZE]
					
			else:
				sculpt_SIZE = BYTES_PER_PLATE
				sculpture = byte_for_plate

			
			selector.write (sculpture)
			PLATE_INDEX_END = selector.tell () - 1
			
			assert (len (sculpture) == sculpt_SIZE)
			
			PROGRESS ({
				"SIZE": sculpt_SIZE,
				"LAST_LOOP": LAST_LOOP,
				"INDEXES": [
					PLATE_INDEX_START,
					PLATE_INDEX_END
				]
			})
			
			if (LAST_LOOP):
				print ("closing sculpt pointer") 
			
				selector.close ()
			
				print ()
				print ("sculpt IS DONE, last_byte =", PLATE_INDEX_END)
				print ()
				
				
				
				return;