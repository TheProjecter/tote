#!/usr/bin/python
days = []
tasks = []
events = []
tomorrows = ["none"]

import datetime

### UTC CLASS. DISABLE IF NECESSARY
#import datetime
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


def convertToSeconds(m=0, h=0, d=0, w=0, y=0):
    return m*60 + h*3600 + d*3600*24 + w*7*24*3600 + y*365*24*3600

def addTime(currentTime, seconds=0):
    import time
    return time.localtime(time.mktime(currentTime) + int(seconds)) #Find time in secs, add needed seconds, convert back into 9field tuple

def dateFromTime(localTime):
    hdate = str(localTime).split()[0].split("-")
    return hdate[0] + "." + hdate[1] + "." + hdate[2]
    #return str(localTime[1]) + "." + str(localTime[2]) + "." + str(localTime[0])

'Sat Apr 21 15:15:52 2007'

def shortTime(theTime):
    theTime = theTime.timetuple()
    longTime = time.asctime(theTime)
    splitTime = longTime.split(" ")
    print splitTime
    shortenedTime = splitTime[1] + " " + splitTime[2] + ", " + splitTime[3].split(":")[0] + ":" + splitTime[3].split(":")[1]
    return shortenedTime

def splitDate(date):  #turns mm.dd.yyyy to [mm, dd, yyyy]
    tempDate = date.split(".")
#    print " Dates are", tempDate[0], tempDate[1], tempDate[2]
    return [int(tempDate[0]), int(tempDate[1]), int(tempDate[2])]

def combineDate(dateSplit): #turns [mm, dd, yyyy] to mm.dd.yyyy
    return str(dateSplit[0]) + "." + str(dateSplit[1]) + "." + str(dateSplit[2])

def daysBetweenDates(date1, date2, inputHandle=0): #Yes, these have to be in order
    import calendar
    if inputHandle == 1:
	date1 = date1.date
	date2 = date2.date
    splitDate1 = splitDate(date1)
    splitDate2 = splitDate(date2)
    daysApart = 0
    if splitDate2[2] != splitDate1[2]:    
       daysApart = daysApart + splitDate2[1] #add days since start of end month
       print "the years are: ", splitDate1[2], splitDate2[2]
       for month in range(1, splitDate2[0]):     #Now for days untill start of year of splitDate2
         daysApart = daysApart + calendar.monthrange(splitDate2[2], month)[1]

       for year in range(splitDate1[2] + 1, splitDate2[2]): # Do years inbetween
         for month in range(1, 13):
            daysApart = daysApart + calendar.monthrange(year, month)[1]

       for month in range((splitDate1[0] + 1), 13): # and add days from months in the previous years. 
	 daysApart = daysApart + calendar.monthrange(splitDate1[2], month)[1]

    elif splitDate2[0] != splitDate1[0]:
        print "The months are: ", splitDate1[0], splitDate2[0]	
        daysApart = daysApart + splitDate2[1] #add days since start of end month
	for month in range(splitDate1[0] + 1, splitDate2[0]):	 
		daysApart = daysApart + calendar.monthrange(splitDate1[2], month)[1]
        # days = days + howmanydays in year of 1, month of 1 - day of 1 #I.E. Days from start date till endofmonth
        daysApart = daysApart + calendar.monthrange(splitDate1[2], splitDate1[0])[1] - splitDate1[1]
    elif splitDate2[1] == splitDate1[1]:
	return 0
    return daysApart

def timeBetweenTimes(time1, time2): # our 9field tuple is time1
    date1 = dateFromTime(time1)
    date2 = dateFromTime(time2)
    days = daysBetweenDates(date1, date2)
    print date1, date2, days
    hours = time2[3] - time1[3]
    minutes = time2[4] - time1[4]
    seconds = convertToSeconds(d=days, h=hours, m=minutes)
    return seconds			


def dayHandleFromDate(dateWanted):
    for each in days:
        print each.date, dateWanted
        if each.date == dateWanted:
            return each
        else:
            pass
    #If we got this far, we didn't find any matching dates.
    return 0
         
def findItemsForDate(date):
    tempItems = get_upcoming_items(-1)
    foundItems = []
    for each in tempItems:
        if each.getdate != date:
            pass
        else:
            print "Leaving: ", each.getdate
            foundItems.append(each)
    return foundItems
    
def findItemsUntilDate(date):
    tempItems = get_upcoming_items(-1)
    for item in tempItems:
        if item.date > date:
            tempItems.pop(tempItems.index(item))
        else:
            pass
    return tempItems
    
    
def searchEventsFor(theKeywords, eventsList):
	theKeywordList = theKeywords.split(" ")
	#Event things we look at:
	# name, description	 
    
def get_upcoming_items(number_of_items):
    fullList = []
    for item in tasks:
        fullList.append(item)
    for item in events:
        fullList.append(item)
    fullList.sort()
    if number_of_items == -1:
        print "Fullist has %s items" % len(fullList)
        return fullList
    tempList = []
    for number in range(number_of_items):
        tempList.append(fullList[number])
    return tempList
    
    
    
#Remove:    
def updateDate(date=-1):
    import time
    if date == -1:
        date = []
        for each in time.localtime():
          date.append(each)
#    if tomorrows[0]. == 
    
#/end remove

class day:
    #Builtin Methods
    def __init__(self, dateTime, startOfDay="0600", endOfDay="2000"): #ie "1124"
        self.startOfDay = startOfDay
        self.endOfDay = endOfDay
        self.dateTime = dateTime
        days.append(self)
        
    def getdate(self):
        hdate = str(self.dateTime).split()[0].split("-")
        return hdate[0] + "." + hdate[1] + "." + hdate[2]
        
    def __lt__(self, secondThing):
        if self.dateTime < secondThing.dateTime:
            return True
        else:
            return False

    def __gt__(self, secondThing):
        if self.dateTime > seconThing.dateTime:
            return True
        else:
            return False


def taskCreator():
	pass	


class task:
    def __init__(self, name, startTime=-1, dueTime=-1, description="", parentEvents=[], resources=[], relatedTasks=[], isProject=0):
        #Setting the dates
        import time
        tasks.append(self)
        self.name = name
        if startTime == -1:
            self.startTime = datetime.datetime.now()
        else:
            try:
                self.startTime = startTime
            except TypeError:
                self.startTime = datetime.datetime.now()
        print self.startTime
        if dueTime == -1:
            self.dueTime = self.startTime.replace(day=self.startTime.day+1) #One day from now
        else:
            
            ############## working on date here. Start of day? End of day? ###################
            try:
                self.dueTime = dueTime
            except TypeError:
                self.dueTime = tstartTime.replace(day=startTime.day+1, hour=7)
        self.relatedTasks = []
        self.resources = []
        self.description = description
        self.progress = 0
        self.isProject = isProject
        self.subTasks = []
        self.parentEvents = []
        for each in relatedTasks:
            self.relatedTasks.append(each)
        for each in resources:
            self.resources.append(each)
        self.parentEvents = []
        for each in parentEvents:
            self.parentEvents.append(each)
        self.dateTime = self.startTime
    
    def getdate(self):
        hdate = str(self.startTime).split()[0].split("-")
        return hdate[0] + "." + hdate[1] + "." + hdate[2]
    
    def __lt__(self, secondThing):
        if self.startTime < secondThing.startTime:
            return True
        else:
            return False

    def __gt__(self, secondThing):
        if self.startTime > secondThing.startTime:
            return True
        else:
            return False
        
    def removeRelatedTask(self, task):
        try:
            return self.relatedTasks.remove(task)
        except ValueError:
            return 0

        
    def removeResource(self, resource):
        try:
            return self.resources.remove(resource)
        except ValueError:
            return 0
        
    def removeFromEvent(self, event): #event handle
        try:
            return self.parentEvents.remove(event)
        except ValueError:
            return 0           

    def duration(self):
        return timeBetweenTimes(self.startTime, self.endTime)


class resource:
#The Idea behind this class is that it is a helper for tasks or events. It provides a way to put other content into Tote. It also lets there be shared resources among different tasks/events. 
	def __init__(self, name, description="A simple resource...", expires=0, attachedTo=[]):
		self.name = name
		self.description = description
		self.expires = expires
		self.attachedTo = []
		for item in attachedTo:
			self.attachedTo.append(item)
		




class event:
    def __init__(self, name, description="", startTime=-1, endTime=-1, isBlock=0):
        events.append(self)
        self.name = name
        self.description = description
        if startTime == -1:
            startTime = datetime.datetime.now()
        else:
            try:
                self.startTime = startTime
            except TypeError:
                startTime = dateTime.datetime.now()
        if endTime == -1:
            endTime = startTime.replace(day=startTime.day+1) #One day from now
        else:
            try:
                self.endTime = endTime
            except TypeError:
                endTime = startTime.replace(day=startTime.day+1) #One day from now
        self.dateTime = self.startTime
        self.isBlock = isBlock
        
    def getdate(self):
        hdate = str(self.startTime).split()[0].split("-")
        return hdate[0] + "." + hdate[1] + "." + hdate[2]
     
    def __lt__(self, secondThing):
        if self.dateTime < secondThing.dateTime:
            return True
        else:
            return False

    def __gt__(self, secondThing):
        if self.dateTime > secondThing.datetime:
            return True
        else:
            return False
        

def timeBetweenEvents(event1, event2):
    if event1.startTime < event2.startTime:
        firstInTime = event1
    else:
        firstInTime = event2
        
import time
## When is an event due?
#5 days...
#endprojecttime = addTime(time.localtime(), convertToSeconds(d=5))
#print endprojecttime
#project1 = event(time.localtime(), endprojecttime)
#print project1.startTime, project1.endTime
#print timeBetweenTimes(time.localtime(), project1.endTime)

#Some Test Days:
day1 = day("04.27.2007")
day2 = day("04.20.2007")
dayandrew = day("09.28.1989", startOfDay="0145", endOfDay="2400")
dayjohn = day("06.29.1992", startOfDay="0550")
dayroy = day("12.01.1947")
daymarleen = day("04.15.1957")

#Some sample Tasks
task1 = task("First", description="A task1", startTime=datetime.datetime.now())
task2 = task("Second", description="A task2", startTime=datetime.datetime.now())
task3 = task("Third", description="A task3", startTime=datetime.datetime.now())
task4 = task("Fourth", description="A task4", startTime=datetime.datetime.now())

#Some Sample Events
event1 = event("First", "Event1", startTime=datetime.datetime.now())
event2 = event("Second", "Event2", startTime=datetime.datetime.now())
event3 = event("Third", "Event3", startTime=datetime.datetime.now())
event4 = event("Fourth", "Event4", startTime=datetime.datetime.now())

def printDays(listOfDays):
	for day in listOfDays:
		print day.date, day.startOfDay, day.endOfDay


