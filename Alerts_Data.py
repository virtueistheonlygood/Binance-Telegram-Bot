import FileIO


ALERTS = dict()

def isAlertsNeedDump():
	temp = FileIO.readFile("alerts.json")
	return not ALERTS==temp
	
def pumpAlerts():
	global ALERTS
	ALERTS = FileIO.readFile("alerts.json")
	
def dumpAlerts():
	FileIO.writeFile(ALERTS,"alerts.json")