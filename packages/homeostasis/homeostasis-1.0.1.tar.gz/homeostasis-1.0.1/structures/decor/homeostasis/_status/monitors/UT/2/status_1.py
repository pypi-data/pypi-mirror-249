

def check_1 ():
	def find_path_status (paths, path_END):
		for path in paths:
			SPLIT = path ["path"].split (path_END)
		
			if (len (SPLIT) == 2 and len (SPLIT [1]) == 0):
				return path 

		print ("path_END:", path_END)
		raise Exception ("path NOT FOUND")
		
	
	print ("test_1")

	import pathlib
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	stasis = normpath (join (THIS_FOLDER, "stasis"))

	import homeostasis
	SCAN = homeostasis.start (
		glob_string = stasis + '/**/*_health.py',
		relative_path = stasis,
		module_paths = [
			#* FIND_STRUCTURE_paths (),			
			normpath (join (stasis, "modules"))
		]
	)
	status = SCAN ['status']
	paths = status ["paths"]
	
	import json
	print ("UT 2 status FOUND", json.dumps (status ["stats"], indent = 4))

	assert (len (paths) == 2)
	assert (status ["stats"]["alarms"] == 0)
	assert (status ["stats"]["empty"] == 1)
	assert (status ["stats"]["checks"]["passes"] == 2)
	assert (status ["stats"]["checks"]["alarms"] == 1)
	
	path_1 = find_path_status (paths, "1_health.py")
	assert (type (path_1) == dict)
	
checks = {
	'check 1': check_1
}