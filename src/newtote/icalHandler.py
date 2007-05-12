import vobject
import datetime
import nuclasses
defaultFolderStructure = [
                            "./data",
                            "./data/default",
                            "./config"]
    
defaultFileStructure = [
                        "./data/default/defaultEventCalendar.ics",
                        "./data/default/defaultTaskCalendar.ics",
                        "./config/default/defaultConfig.conf"]



### UTC CLASS. DISABLE IF NECESSARY
import datetime

ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)

# A UTC class.

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()
#####



class Session:
    def __init__(self, dataFiles=defaultFileStructure, configFile=0):
	pass


def exportEventsToiCal(list_of_events):
    pass


class iCal:
    pass


def createToteDirs(path="~/.tote"):
    ### (path is most likely "~/.tote")
    import os
    fullpath = os.path.expanduser(path)
    if os.path.isdir(fullpath):  #This is if there is already a tote folder
        os.chdir(fullpath)
    else:                        #Otherwise we need to create one
        splitPath = fullpath.split("/")
        os.chdir(os.path.expanduser("~/"))
        os.mkdir(splitPath[-1])
        os.chdir(splitPath[-1])
    if os.getcwd != fullpath:
        os.chdir(fullpath)
    for folder in folderStructure:
        os.mkdir(folder)
    for file in fileStructure:
        temp = open(file, 'w')
        temp.close()

        
    
                
def eventToiCal(ical, event):
	ical.add('vevent')
	ical.vevent.add('summary').value = event.name
	icalstart = ical.vevent.add('dtstart')
	print icalstart
	ical.prettyPrint()
    

def removeToteDirs(path):
    pass


cal = vobject.newFromBehavior('vcalendar')
print cal.behavior


ical = vobject.iCalendar()
print ical

ical.add('vevent')
ical.vevent.add('summary').value = "Hey there folks"
ical.prettyPrint()

print utc

icalStart = ical.vevent.add('dtstart')
icalStart.value = datetime.datetime(2006, 2, 16, 0)
print "amhere"
ical.prettyPrint()

card = vobject.vCard()
print card.behavior


eventToiCal(ical, nuclasses.events[2])

