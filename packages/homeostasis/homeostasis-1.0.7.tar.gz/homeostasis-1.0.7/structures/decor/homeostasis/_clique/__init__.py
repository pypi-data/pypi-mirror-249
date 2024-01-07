







from .group import clique as clique_group

def clique ():
	print ("clique")

	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("shares")
	def shares ():
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
	@click.command ("homeostasis")
	def homeostasis_homeostasis ():
		import homeostasis._status.establish as establish_status
		establish_status.start ()
	

	import click
	@click.command ("status")
	@click.option ('--simultaneous', default = "yes")
	def status (simultaneous):
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		import os
		CWD = os.getcwd ()
		
		if (simultaneous == "yes"):
			simultaneous_bool = True
		elif (simultaneous == "no"):
			simultaneous_bool = False
		else:
			print ("'--simultaneous yes' or '--simultaneous no'")
			exit ()
			

		import homeostasis
		homeostasis.start (
			glob_string = CWD + '/**/status_*.py',
			simultaneous = simultaneous
		)


	group.add_command (shares)	
	group.add_command (homeostasis_homeostasis)	
	group.add_command (status)
	
	group.add_command (clique_group ())
	group ()




#
