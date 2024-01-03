

import earring.node.flask as node_flask

def start (
	port
):
	print ('starting')
	
	app = node_flask.build ()
	app.run (port = port)

	return;