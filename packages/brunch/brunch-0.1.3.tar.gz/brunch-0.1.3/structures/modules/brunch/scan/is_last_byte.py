
'''
	last_byte_index might be equal to the drive size.
'''

'''
	import brunch.scan.is_last_byte as is_last_byte
	[ is_last, note ] = is_last_byte.deem ({
		"drive path": drive_path,
		"last_byte": last_byte_index + 1
	})
	if (is_last == False):
		print (note)
'''

'''
	similar:
		[ZSH] fdisk -l
		[ZSH] lsblk -b -p
	
		example:
			last_byte = 2032664576
	
			xxd -len 100 -seek 2032664577 /dev/sdb
			# xxd: Sorry, cannot seek.
			
			xxd -len 100 -seek 2032664576 /dev/sdb
			#
			
			before end:
				xxd -len 100 -seek 2032664575 /dev/sdb
				# 7927ffff: 18
				
				with open ("/dev/sdb", "rb") as f:
					f.seek (2032664575)
					print (f.read (20))
					
					# b'\x18'
					
			
			byte at index 1:
				
				#
				#	00000000: 0002 0406 080a 0c0e 1012 0002 0406 080a  ................
				#
				
				with open ("/dev/sdb", "rb") as f:
					f.seek (1)
					print (f.read (1))
					
					# b'\x02'
'''
def is_after_end (f, last_byte_index):
	try:
		f.seek (last_byte_index)
		print (f"The last_byte, { last_byte_index }, could be found with seek.")		
	except Exception as E:
		print ("is_after_end exception:", E)
		return True
		
	return False

def if_before_end (f, last_byte_index):
	try:
		f.seek (last_byte_index)
		plate = f.read (2)
		
		print ("plate:", plate)
		
		if (len (plate) == 0):
			return False;
			
		print (f"'{ len (PLATE) }' bytes could be read before the last_byte provided")
		
	except Exception as E:
		print ("if_before_end exception:", E)
		pass;
				
	return True


def deem (params):
	print ()

	drive_path = params ["drive path"]
	last_byte_index = params ["last_byte"]

	print (f"This checks if { last_byte_index } is in fact the last byte.")


	'''
	
	'''
	with open (drive_path, "rb") as f:
		if (is_after_end (f, last_byte_index)):
			return [ False, "The last byte declared is after the last byte." ]
		
		f.close ()
		
	print ("[check passed] The last byte declared isn't after the last byte.")
	
	with open (drive_path, "rb") as f:
		if (if_before_end (f, last_byte_index)):
			return [ False, "The last byte declared is before the last byte." ]
			
		f.close ()

	print ("[check passed] The last byte declared isn't before the last byte.")

	return [ True, "" ]