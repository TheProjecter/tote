import vobject
defaultFolderStructure = [
                            "./data",
                            "./data/default",
                            "./config"]
    
defaultFileStructure = [
                        "./data/default/defaultEventCalendar.ics",
                        "./data/default/defaultTaskCalendar.ics",
                        "./config/default/defaultConfig.conf"]


class Session:
    def __init__(self, dataFile=defaultDataFile, configFile=0):



def exportEventsToiCal(list_of_events):
    pass


class iCal:
    pass


def createToteDirs(path="~/.tote"):
    ### (path is most likely "~/.tote")
    import os
    fullpath = os.path.expanduser(path)
    if os.path.isdir(fullpath)  #This is if there is already a tote folder
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
        
    
                
        
    

def removeToteDirs(path):
    


cal = vobject.newFromBehavior('vcalendar')
print cal.behavior


ical = vobject.iCalendar()
print ical

ical.add('vevent')
ical.vevent.add('summary').value = "Hey there folks"
ical.prettyPrint()

icalStart = ical.vevent.add('dtstart')


card = vobject.vCard()
print card.behavior

icalStart.value = datetime(2006, 2, 16, tzinfo = utc)
ical.prettyPrint()