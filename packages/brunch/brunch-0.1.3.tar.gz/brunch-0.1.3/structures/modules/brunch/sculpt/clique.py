





def sculpt_options (GROUP):
	import click
	@GROUP.group ("sculpt")
	def GROUP ():
		pass
		
	import click
	@GROUP.command ("ENTIRE-DRIVE")
	@click.option ('--drive-path', required = True, help = '')
	@click.option ('--drive-bytes', required = True, help = '')
	def EXAMPLE (port):	
		


		return;
		
		
	'''
		brunch sculpt BYTES --drive-path /dev/sde --index-0 31914983423 --index-1 31914983423 --hex-string '04'
	'''
	import click
	@GROUP.command ("BYTES")
	@click.option ('--drive-path', required = True, help = '')
	@click.option ('--index-0', required = True, help = '')
	@click.option ('--index-1', required = True, help = '')
	@click.option ('--hex-string', required = True, help = '')
	def sculpt_BYTES (drive_path, index_0, index_1, hex_string):	
		import brunch.sculpt as sculpt

		BYTES_FOR_PLATE = bytes.fromhex (hex_string)
		
		print (BYTES_FOR_PLATE)
		print (type (BYTES_FOR_PLATE))
		

		sculpt.START ({
			"DRIVE PATH": drive_path,
			
			"BYTES INDEXES": [ 
				int (index_0), 
				int (index_1)
			],		
			"BYTES FOR PLATE": BYTES_FOR_PLATE,
			
			"PROGRESS": lambda PARAMS : (print (PARAMS))
		})

		return;

	return;
