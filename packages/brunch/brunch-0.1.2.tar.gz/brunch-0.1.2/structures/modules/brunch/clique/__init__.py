

'''
	import brunch.clique as clique
'''

from brunch.sculpt.clique import sculpt_options
from brunch.scan.clique import scan_clique
from brunch.erase.clique import erase_options

def clique ():

	import click
	@click.group ()
	def group ():
		pass

	
	import click
	@click.command ("ping")
	@click.option ('--port', required = True, help = '')
	def ping (port):
		print ('pong!')
		
		import requests
		r = requests.get (f'http://127.0.0.1:{ port }')
		
		return;
	group.add_command (ping)
	
	import click
	@click.command ("shares")
	def shares ():	
		print ("shares")

		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		print (f"opening shares from '{ this_module }'")

		import shares
		shares.start ({
			"directory": this_module,
			"extension": ".s.HTML",
			"relative path": this_module
		})


		return;
	group.add_command (shares)

	sculpt_options (group)
	scan_clique (group)
	erase_options (group)

	group ()
