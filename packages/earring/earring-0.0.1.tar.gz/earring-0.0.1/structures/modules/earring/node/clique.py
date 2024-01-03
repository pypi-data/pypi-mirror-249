



import earring.node.flask.start_dev as flask_start_dev

def clique ():
	import click
	@click.group ("node")
	def group ():
		pass

	'''
		./earring node start -np 43123
	'''
	import click
	@group.command ("start")
	@click.option ('--node-port', '-np', default = '43123')
	def search (node_port):		
		flask_start_dev.start (
			port = int (node_port)
		)
	
		return;

	return group




#



