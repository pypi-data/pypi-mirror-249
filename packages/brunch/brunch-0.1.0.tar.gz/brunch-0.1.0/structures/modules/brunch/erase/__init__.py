
'''
	VENTURES:
		
		from brunch.erase import erase
		from brunch.sculpt.strategies.strategy_1 import strategy_1
		from brunch.sculpt.strategies.strategy_2 import strategy_2
		
		erase ({
			"skip over": 0,
			
			"DRIVE PATH": drive_path,
			"last_byte": last_byte,
			
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
'''

import brunch.scan as scan
import brunch.scan.is_last_byte as is_last_byte
import brunch.sculpt as sculpt

from fractions import Fraction
from time import sleep, perf_counter
import datetime

def drive_found (drive_path):
	import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
	drive_bytes = LS_BLK_calc_size.solidly (
		drive_path = drive_path
	)


def erase (cargo):
	

	'''
		skip_over = 0	-> SKIPS NOTHING
		skip_over = 1 -> SKIPS FIRST sculpt
		skip_over = 2 -> SKIPS TO SECOND LOOP
	'''	

	if ("skip over" not in cargo):
		skip_over = 0
	else:
		skip_over = cargo ["skip over"]

	drive_path = cargo ["DRIVE PATH"]
	drive_found (drive_path = drive_path)
	
	last_byte = cargo ["last_byte"]
	sculpt_strategies = cargo ["sculpt"]["strategies"]

	#
	#
	sculpt_START = 0
	#
	#

	'''
	[ is_last, note ] = is_last_byte.deem ({
		"drive path": drive_path,
		"last_byte": last_byte + 1
	})
	if (is_last == False):
		raise Exception (note)
	'''
	
	#print ("last_byte is_last:", is_last)
	

	'''
	
	'''
	sculpt_loop = 1
	def sculpt_progress (PARAMS):
		nonlocal sculpt_loop;
		
		INDEXES = PARAMS ["INDEXES"]
		SIZE = PARAMS ["SIZE"]
		LAST_LOOP = PARAMS ["LAST_LOOP"]

		if (sculpt_loop == 1000 or LAST_LOOP == True):
			percent = 100 * Fraction (INDEXES [1] / last_byte)			
			if (percent.denominator == 1):
				percent = str (int (percent))
			else:
				percent = str (float (percent))
			
			
			#BYTE_INDEX = "[AT BYTE INDEX:" + str (INDEXES[0]) + "]"
			plate_size = "[reached byte index:" + str(INDEXES[0]) + "]"
			percent_STRING = "[" + percent + "%]"
			
			now = datetime.datetime.now (
				tz = datetime.timezone.utc
			).replace (microsecond = 0).isoformat()
			
			print (
				"sculpting:",
				now,
				plate_size,
				percent_STRING
			)
			
			sculpt_loop = 1;
		
		sculpt_loop += 1

	STAGE = 1;
	LOOP_COUNT = 1;
	for strategy in sculpt_strategies:
		print (f"loop '{ LOOP_COUNT }' of '{ len (sculpt_strategies) }'")
	
		#strategy_bytes_per_plate = strategy ["bytes per plate"]
		BYTES = strategy ["BYTES"]
		
		#print ("strategy_bytes_per_plate", strategy_bytes_per_plate)
		#print ("BYTES", len (BYTES))
		
		strategy_bytes_per_plate = len (BYTES)
		
		#
		#	skip_over = 0, STAGE = 1	->	DON'T SKIP
		#	skip_over = 1, STAGE = 1	->	SKIP
		#	skip_over = 2, STAGE = 1	->  SKIP
		#
		#	skip_over = 2, STAGE = 3	-> 	DON'T SKIP
		#
		if (STAGE > skip_over):
			PLACE_1 = perf_counter ()

			sculpt.START ({
				"DRIVE PATH": drive_path,
				
				"BYTES INDEXES": [ 0, last_byte ],			
				"BYTES FOR PLATE": BYTES,
				
				"PROGRESS": sculpt_progress
			})
			
			ELAPSED = perf_counter () - PLACE_1
			
			print ("Sculpt required", ELAPSED, "seconds.")
			
		else:
			print ("SKIPPING sculpt, STAGE = ", STAGE)
			
		STAGE += 1;
		
		if (STAGE > skip_over):
			
		
			scan_loop = 1
			def scan_PROGRESS (PARAMS):
				nonlocal scan_loop;
			
				PLATE = PARAMS ["PLATE"]
				scan_SIZE = PARAMS ["scan SIZE"]
				INDEXES = PARAMS ["INDEXES"]
				LAST_scan = PARAMS ["LAST scan"]
				
				#
				#	? BYTE_STRING_EQ
				#
				
				
				if (PLATE != BYTES [0:scan_SIZE]):
					BYTES_PARTIAL = BYTES [0:scan_SIZE]
				
					print ("PLATE LEN:", len (PLATE))
					print ("BYTES LEN:", len (BYTES_PARTIAL))
					
					if (len (PLATE) != len (BYTES_PARTIAL)):
						assert (len (PLATE) != len (BYTES_PARTIAL))
					
					
					INDEX = 0;
					LAST_INDEX = len (PLATE) - 1
					while (INDEX <= LAST_INDEX):
						if (PLATE [ INDEX ] != BYTES_PARTIAL [INDEX]):
							print ("INEQUALITY AT INDEX:", INDEX, PLATE[INDEX], BYTES_PARTIAL[INDEX])
							
						INDEX += 1
					
					assert (PLATE == BYTES [0:scan_SIZE])
				
				
				if (scan_loop % 1000 == 0 or LAST_scan == True):
					percent = 100 * Fraction (INDEXES [1] / last_byte)
					if (percent.denominator == 1):
						percent = str (int (percent))
					else:
						percent = str (float (percent))
					
					BYTE_INDEX = "[REACHED BYTE INDEX:" + str (INDEXES[0]) + "]"
					percent_STRING = "[" + str (percent) + "%]"
								
					SIZE = "[scan SIZE: " + str (scan_SIZE) + "]"			
								
					CONTENT = "[FIRST 16 BYTES: " + PLATE[0:16].hex () + "]"
								
					print (
						"scanNING:",
						BYTE_INDEX,
						CONTENT,
						percent_STRING
					)
					
				scan_loop += 1
				
			PLACE_1 = perf_counter ()	
				
			scan.START ({
				"DRIVE PATH": drive_path, 
				
				"BYTES INDEXES":  [ 0, last_byte ],	
				"bytes per plate": strategy_bytes_per_plate,
				
				"PROGRESS": scan_PROGRESS
			})
			
			ELAPSED = perf_counter () - PLACE_1
			
			print ("Scan required", ELAPSED, "seconds.")
		else:
			print ("SKIPPING scan, STAGE = ", STAGE)
			
		STAGE += 1

		LOOP_COUNT += 1
		


	return
