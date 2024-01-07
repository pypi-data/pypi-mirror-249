
'''
	env drive_path=/dev/sd_ python3 status.proc.py '_status/status_shell/s1/status_1.py'
'''

import brunch.decor as decor
import brunch._status.status_shell.s1.flask_server as flask_server

import time

def check_1 ():	
	estate = decor.estate ()
	vibe = estate ['vibe'] ()	
	
	local_shell = vibe ["local shell"]	

	print ("local_shell", local_shell)
	
	
	was_called = False;
	def called ():
		print ('from the called def')
		
		nonlocal was_called;
		was_called = True;
		
		return

	import threading
	threading.Thread (
		target = flask_server.start,
        kwargs = {
			'called': called
		}
    ).start ()

	import _thread as thread
	#thread.start_new_thread (flask_server.start, ())
	
	print ()
	print ('waiting for server to start')
	print ()
	
	time.sleep (1)
	
	import subprocess
	outlet = subprocess.Popen (
		#[f"'{ local_shell }'", "ping", "--port", "34783"],
		[ local_shell, "ping", "--port", "34783"]		
	)

	time.sleep (1)


	assert (was_called == True), was_called

	return;
	
	
checks = {
	'check 1': check_1
}