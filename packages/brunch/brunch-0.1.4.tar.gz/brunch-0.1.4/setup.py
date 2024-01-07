
'''
	pip install --upgrade setuptools

	(rm -rf dist && python3 -m build --sdist && twine upload dist/*)
'''
#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages

version = "0.1.4"
name = 'brunch'
install_requires = [
	'homeostasis',

	'shares',
	'ships',
	'flask',

	'jsonschema',
	'rich'
]

def scan_description ():
	try:
		with open ('structures/modules/brunch/brunch.s.HTML') as f:
			return f.read ()

	except Exception as E:
		pass;
		
	return '';


setup (
    version = version,

	name = name,
    install_requires = install_requires,	
	
	package_dir = { 
		'brunch': 'structures/modules/brunch'
	},
	scripts = [ 
		'structures/scripts/brunch' 
	],
	
	include_package_data = True,
	package_data = {
		"": [ "*.s.HTML" ]
    },
	
	license = "CL",
	long_description = scan_description (),
	long_description_content_type = "text/plain",
)
