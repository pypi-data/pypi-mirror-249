




from earring._clique.group import clique as clique_group

from earring.node.clique import clique as node_clique
from earring.safe.clique import clique as safe_clique

def clique ():

	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

	group.add_command (example_command)

	group.add_command (node_clique ())
	group.add_command (safe_clique ())
	
	
	group ()




#
