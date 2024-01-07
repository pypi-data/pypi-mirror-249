


def start (
	called = None
):
	from flask import Flask

	app = Flask (__name__)

	@app.route ("/")
	def hello_world():
		print ("called!");
		
		called ()
		
		return ''
		
	app.run (
		port = 34783
	)