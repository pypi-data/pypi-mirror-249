







from .group import clique as clique_group

def clique ():
	print ("clique")

	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("shares")
	def example_command ():
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		import shares
		shares.start ({
			"directory": this_module,
			"extension": ".s.HTML",
			"relative path": this_module
		})
	

	import click
	@click.command ("status")
	def example_command ():
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		import os
		CWD = os.getcwd ()

		import homeostasis
		homeostasis.start (
			glob_string = CWD + '/**/status_*.py',
			simultaneous = True
		)


	group.add_command (example_command)

	group.add_command (clique_group ())
	group ()




#
