



def add_paths_to_py (paths):
	import pathlib
	from os.path import dirname, join, normpath
	import sys

	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))

add_paths_to_py ([
	'../../../modules',
	'../../../modules_pip'
])


def calc_drive_path ():
	import os
	drive_path = os.environ.get ('drive_path')
	print ("drive path:", drive_path)
	if (type (drive_path) != str or len (drive_path) == 0):
		print ("A 'drive' path needs to be designated.")
		print ()
		print ("	Caution, example: 'env drive_path=/dev/sd_ drive_bytes= python3 status.py'")
		print ()

		exit ()
		
	return drive_path


def calc_drive_bytes ():
	import os

	#
	#	   40 GB ~= 40000000000
	#	 	1 GB ~=  1000000000
	#	 1/10 GB ~=   100000000	
	#
	drive_bytes = int (os.environ.get ('drive_bytes'))
	assert (drive_bytes >= 100000000)

	print ("drive_bytes:", drive_bytes)
	
	return drive_bytes;
	
def calc_is_advanced ():
	import os
	is_advanced = os.environ.get ('advanced')	
	return is_advanced;


def start (
	glob_string = "",
	restaurant = ""
):
	import brunch.modules.LS_BLK.calc_size as LS_BLK_calc_size
	drives_bytes = LS_BLK_calc_size.solidly (
		drive_path = "/dev/sdb"
	)
	
	print ("drives_bytes:", drives_bytes)
	


	drive_path = calc_drive_path ()
	#drive_bytes = calc_drive_bytes ()
	is_advanced = calc_is_advanced ()

	print ("is_advanced:", is_advanced)

	import pathlib
	from os.path import dirname, join, normpath
	this_directory = pathlib.Path (__file__).parent.resolve ()

	this_modules = normpath (join (this_directory, ".."))
	module_bases = normpath (join (this_directory, "../.."))
	
	if (is_advanced == "yes"):
		status = normpath (join (this_directory, "status_advanced"))

	import sys
	if (len (sys.argv) >= 2):
		glob_string = this_modules + '/' + sys.argv [1]
	else:
		glob_string = this_modules + '/**/status_*.py'

	import rich
	rich.print_json (data = {
		"glob_string": glob_string		
	})

	from os.path import dirname, join, normpath

	import homeostasis
	scan = homeostasis.start (
		glob_string = glob_string,	
		module_paths = [
			normpath (join (module_bases, "modules")),
			normpath (join (module_bases, "modules_pip"))
		],
		relative_path = this_modules
	)


start ()