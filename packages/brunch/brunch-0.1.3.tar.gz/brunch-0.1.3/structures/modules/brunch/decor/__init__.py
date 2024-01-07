


'''
	agenda:
	
		import brunch.decor as decor
		estate = decor.estate ()
		
		vibe = estate ['vibe'] ()	
		local_shell = vibe ["local shell"]	
		
'''

def estate ():
	import pathlib
	from os.path import dirname, join, normpath
	import sys

	this_directory = pathlib.Path (__file__).parent.resolve ()	

	decor = {
		"local shell": str (normpath (join (this_directory, "..", "brunch_local")))
	}

	def vibe ():
		return decor
	
	'''
	def modeify (label, feeling):
		nonlocal decor;
		decor [ label ] = feeling
	'''
	
	return {
		'vibe': vibe,
		
		#'modeify': modeify
	}