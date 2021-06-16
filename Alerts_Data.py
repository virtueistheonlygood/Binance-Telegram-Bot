import FileIO


ALERTS = dict()

def pumpAlerts():
	global ALERTS
	ALERTS = FileIO.readFile("alerts.json")
	
def dumpAlerts():
	FileIO.writeFile(ALERTS,"alerts.json")