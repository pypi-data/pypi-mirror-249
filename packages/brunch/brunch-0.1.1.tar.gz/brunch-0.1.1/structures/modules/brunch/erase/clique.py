

import json

def erase_options (GROUP):
	import click
	@GROUP.group ("erase")
	def GROUP ():
		pass
		
	'''
		brunch erase entirely --drive-path /dev/sde --last-byte-index 40018599423
		brunch erase entirely --drive-path /dev/sde --last-byte-index 32010928127
	'''
	'''
		last_byte_index might be equal to the drive size.
	'''
	import click
	@GROUP.command ("entirely")
	@click.option ('--drive-path', required = True, help = '')
	@click.option ('--skip-over', default = 0, help = '')
	@click.option ('--last-byte', default = '', help = '')
	def erase_entirely (drive_path, skip_over, last_byte):	
		from brunch.erase import erase
		from brunch.sculpt.strategies.strategy_1 import strategy_1
		from brunch.sculpt.strategies.strategy_2 import strategy_2
				
		if (len (last_byte) >= 1):
			drive_bytes = int (last_byte)
		
		else:
			import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
			drive_bytes = LS_BLK_calc_size.solidly (
				drive_path = drive_path
			)
			
			import brunch.scan.is_last_byte as is_last_byte
			[ is_last, note ] = is_last_byte.deem ({
				"drive path": drive_path,
				"last_byte": drive_bytes
			})
			if (is_last == False):
				raise Exception (note)		
			
		erase ({
			"SKIP OVER": int (skip_over),
			
			"DRIVE PATH": drive_path,
			"last_byte": int (drive_bytes - 1),
			
			"sculpt": {
				"strategies": [{
					#"bytes per plate": 512 * 512,
					"BYTES": strategy_1 ()
				},{
					#"bytes per plate": 512 * 512,
					"BYTES": strategy_2 ()
				}]
			}
		})
		
		
		return;

	return;
