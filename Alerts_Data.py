import FileIO


ALERTS = dict()

def isAlertsNeedDump():
	temp = FileIO.readFile("alerts.json")
	return not ALERTS==temp
	
def pumpAlerts():
	print("Reading All Alerts from file")
	global ALERTS
	ALERTS = FileIO.readFile("alerts.json")
	
def dumpAlerts():
	print("Writing Alters to File")
	FileIO.writeFile(ALERTS,"alerts.json")