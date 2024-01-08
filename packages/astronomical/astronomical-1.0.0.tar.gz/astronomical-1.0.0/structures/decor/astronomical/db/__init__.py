

'''
	import astronomical.db as astronomical_db
	records = astronomical_db.records (
		db_directory = normpath (join (dynamics, f"status_db"))
	)
'''

'''
	import astronomical.db as astronomical_db
	last_record = astronomical_db.last_record (
		db_directory = normpath (join (dynamics, f"status_db"))
	)
'''

from tinydb import TinyDB, Query

def records (
	db_directory
):
	import pathlib
	from os.path import dirname, join, normpath
	db_file = normpath (join (db_directory, f"records.json"))
	db = TinyDB (db_file)

	records = db.all ()
	db.close ()
	
	return list (records)
	
	
def last_record (
	db_directory
):
	import pathlib
	from os.path import dirname, join, normpath
	db_file = normpath (join (db_directory, f"records.json"))
	db = TinyDB (db_file)

	records = db.all ()
	db.close ()
	
	records_list = list (records);
	
	return records_list [ len (records_list) - 1 ]