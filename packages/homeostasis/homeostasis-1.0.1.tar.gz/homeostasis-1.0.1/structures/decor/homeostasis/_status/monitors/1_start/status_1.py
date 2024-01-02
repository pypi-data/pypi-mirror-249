




import pathlib
from os.path import dirname, join, normpath
this_folder = pathlib.Path (__file__).parent.resolve ()

chassis = normpath (join (this_folder, "chassis"))
monitors = str (normpath (join (this_folder, "monitors")))
	
import homeostasis
import json

def check_1 ():
	glob_string = chassis + '/**/monitor_*.py'
	
	scan = homeostasis.start (
		glob_string = glob_string,
		simultaneous = True,
		module_paths = [
			normpath (join (chassis, "modules"))
		],
		relative_path = chassis
	)
	
	print (
		json.dumps (
			scan ["stats"], 
			indent = 4
		)
	)
		
	assert (
		scan ["stats"] == {
			"alarms": 0,
			"empty": 0,
			"checks": {
				"passes": 1,
				"alarms": 0
			}
		}
	)
		
checks = {
	'check 1': check_1
}