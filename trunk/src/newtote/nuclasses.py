#!/usr/bin/python
days = []
tasks = []
events = []
blocks = []
tomorrows = ["none"]

import datetime
from random import randint
from socket import gethostname
import uuid

### UTC CLASS. DISABLE IF NECESSARY
#import datetime
ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)


(
    SINGLE,
    DAILY,
    WEEKLY,
    MONTHLY,
    YEARLY
) = range(5)

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


def log_error(error_text):
    print "ERROR: ", error_text

def log_info(info_text):
    print "LOG: ", info_text

def convertToSeconds(m=0, h=0, d=0, w=0, y=0):
    return m*60 + h*3600 + d*3600*24 + w*7*24*3600 + y*365*24*3600

def secondsToHours(seconds, round):
    if round:
        hours = seconds/3600
    elif not round:
        hours = seconds/3600.
    
    return hours

def secondsToHoursMinutes(seconds, round):
    h = seconds/3600.
    hours = int(h)
    remaining_seconds = (h - hours)*3600
    if round:
        minutes = remaining_seconds/60
    elif not round:
        minutes = remaining_seconds/60.
    return (hours, minutes)
        

def addTime(currentTime, seconds=0):
    import time
    return time.localtime(time.mktime(currentTime) + int(seconds)) #Find time in secs, add needed seconds, convert back into 9field tuple

def dateFromTime(localTime):
    hdate = str(localTime).split()[0].split("-")
    return hdate[0] + "." + hdate[1] + "." + hdate[2]
    #return str(localTime[1]) + "." + str(localTime[2]) + "." + str(localTime[0])

'Sat Apr 21 15:15:52 2007'

def shortTime(theTime):
    if theTime == None:
        return None
    theTime = theTime.timetuple()
    longTime = time.asctime(theTime)
    splitTime = longTime.split(" ")
    for each in splitTime:
        if each == "":
            splitTime.remove(each) #For some reason, extra spaces sometimes enter
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

def generateUID():
    uid_date = str(datetime.datetime.now())
    uid_random = str(randint(10000, 99999))
    uid_machine = str(gethostname())
    uid_full = uid_date + "-" + uid_random + "@" + uid_machine
    return uid_full

def taskFromUid(uid):
    for each in tasks:
        if each.uid.__str__() == uid:
            return each
        else:
            pass
    return None

def eventFromUid(uid):
    for each in events:
        if each.uid.__str__() == uid:
            return each
        else:
            pass
    return None

def blockFromUid(uid):
    for each in blocks:
        if each.uid.__str__() == uid:
            return each
        else:
            pass
    return None

#def blipFromUid(uid):
#    for each in blips:
#        if each.uid.__str__() == uid:
#            return each
#        else:
#            pass
#    return None

def blipFromUid(uid, block=None):
    def findBlips(uid, block):
        for blip in block.all_blips:
            if blip.uid.__str__() == uid:
                return (blip)
            else:
                pass
        return None
    if block == None:
        for each in blocks:
            findBlip(uid, each)
    else:
        findBlip(uid, block)
        
        
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


def tomorrowDateTime(today):
    try:
        Tomorrow = today.replace(day=today.day+1) #One day from now
    except ValueError:
        try:
            Tomorrow = today.replace(day=1, month=today.month+1)
        except ValueError: # Yay! we reached dec. 31
            Tomorrow = today.replace(day=1, month=1, year=today.year+1)
    return Tomorrow

class task:
    def __init__(self, name, startTime=-1, dueTime=None, description="", parentEvents=[], parentTask=-1, resources=[], relatedTasks=[], isProject=0, uid=-1, zohoID=None):
        self.__name__ = "task"
        if uid == -1:
            self.uid = uuid.uuid1()
        else:
            self.uid = uuid.UUID(uid)
        otherTask = taskFromUid(self.uid)   #Check to see if we already have a task w/ this uid. If so, then return that one instead
        if otherTask != None:
            return otherTask
        self.zohoID = zohoID
        #Setting the dates
        import time
        tasks.append(self)
        self.name = name
        if parentTask == -1:
            self.parentTask = None
        else:
            self.parentTask = parentTask
        if startTime == -1:
            self.startTime = datetime.datetime.now()
        else:
            try:
                self.startTime = startTime
            except TypeError:
                self.startTime = datetime.datetime.now()
        print self.startTime
        try:
            self.dueTime = dueTime
        except TypeError:
            self.dueTime = None
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

    def get_data(self, thing):
        try:
            return self.data[thing]
        except KeyError:
            log_error("The Requested pice of Data (%s) was not found in the dictionary!" % thing)
            return None

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
		
def time_in_use(day, time, endTime=-1):
    pass #This will use the blocks/events/tasks to determine if the time is in use

class blip:
    def __init__(self, startTime, endTime, uid=-1, repition_type=SINGLE, repition_details=-1):
        self.__name__ = "blip"
        if uid == -1:
            self.uid = uuid.uuid1()
        else:
            self.uid = uuid.UUID(uid)
        otherblip = blipFromUid(self.uid)
        if otherblip != None:
            return otherblip
        self.startTime = startTime
        self.endTime = endTime
        self.repeat=(int(repition_type), int(repition_details))



class block:
    def __init__(self, name, description="", uid=-1):
        self.__name__ = "block"
        if uid == -1:
            self.uid = uuid.uuid1()
        else:
            self.uid = uuid.UUID(uid)
        otherBlock = blockFromUid(self.uid)   #Check to see if we already have a task w/ this uid. If so, then return that one instead
        if otherBlock != None:
            return otherBlock
        
        self.name = name
        self.description = description

        self.single_blips = []
        self.daily_blips = []
        self.weekly_blips = []
        self.monthly_blips = []
        self.yearly_blips = []
        self.all_blips = []
        self.all_blip_types = (self.single_blips,
                               self.daily_blips,
                               self.weekly_blips,
                               self.monthly_blips,
                               self.yearly_blips)
        
    def add_single_blip(self, day, startTime, endTime):
        theblip = blip(startTime, endTime, repition_type=SINGLE, repition_details=day)
        self.single_blips.append(theblip)
        self.all_blips.append(theblip)
    def add_daily_blip(self, startTime, endTime):
        theblip = blip(startTime, endTime, repition_type=DAILY)
        self.daily_blips.append(theblip)
        self.all_blips.append(theblip)
    def add_weekly_blip(self, dayOfWeek, startTime, endTime):
        theblip=blip(startTime, endTime, reptition_type=WEEKLY, repition_details=dayOfWeek)
        self.weekly_blips.append(theblip)
        self.all_blips.append(theblip)
    def add_monthly_blip(self, dayOfMonth, starTime, endTime):
        theblip = blip(startTime, endTime, repition_type=MONTHLY, repition_details=dayOfMonth)
        self.monthly_blips.append(theblip)
        self.all_blips.append(theblip)
    def add_yearly_blip(self, (dayOfMonth, monthOfYear), startTime, endTime):
        theblip = blip(startTime, endTime, repition_type=YEARLY, repition_details=(dayOfMonth, monthOfYear))
        self.yearly_blips.append(theblip)
        self.all_blips.append(theblip)

        
    def remove_blip_from_uid(self, uid):
        blip = blipFromUid(uid, block)
        self.remove_blip(blip)
        
    def remove_blip(self, blip):
        (repition, data) = blip.repeat
        self.all_blips.remove(blip)
        self.all_blip_types[repition].remove(blip)
        
    def list_blips_for_day(self, day): #Day will be in the format datetime.datetime
        matching_blips = []
        for ablip in self.all_blips: #We look at each blip, and pass it to the helper program to determine if it happens on the specified date
            if blip_happens_on_date(ablip, day):
                matching_blips.append(ablip)
            else:
                pass
        return matching_blips
            
def blip_happens_on_date(blip, date):
    day = date.day
    month = date.month
    year = date.year
    if blip.repeat[0] == SINGLE:
        if blip.repeat[1].day == date.day & blip.repeat[1].month == date.month & blip.repeat[1].year == date.year:
            return True
        else:
            return False
    elif blip.repeat[0] == DAILY:
        return True #This has to be true because it happens every day.
    elif blip.repeat[0] == WEEKLY:
        if blip.repeat[1].weekday() == date.weekday():
            return True
        else:
            return False
    elif blip.repeat[0] == MONTHLY:
        if blip.repeat[1] == date.day:
            return True
        else:
            return False
    elif blip.repeat[0] == YEARLY:
        if blip.repeat[1][0] == date.day & blip.repeat[1][1] == date.month:
            return True
        else:
            return False
    else:
        log_error("Blip isn't one of the known repitions. Its value is %s, not 0-4" % blip.repeat[0])
        
    
    


class event:
    def __init__(self, name, description="", startTime=-1, endTime=-1, isBlock=0, uid=-1):
        self.__name__ = "event"
        if uid == -1:
            self.uid = uuid.uuid1()
        else:
            self.uid = uuid.UUID(uid)
        otherEvent = eventFromUid(self.uid)   #Check to see if we already have a task w/ this uid. If so, then return that one instead
        if otherEvent != None:
            return otherEvent
        
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
            try:
                endTime = startTime.replace(day=startTime.day+1) #One day from now
            except ValueError:
                try:
                    endTime = startTime.replace(day=1, month=startTime.month+1)
                except ValueError: # Yay! we reached dec. 31
                    endTime = startTime.replace(day=1, month=1, year=startTime.year+1)
        
        else:
            try:
                self.endTime = endTime
            except TypeError:
                endTime = startTime.replace(day=startTime.day+1) #One day from now
        self.dateTime = self.startTime
        self.isBlock = isBlock
        self.uid = uuid.uuid1()
        
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
#day1 = day("04.27.2007")
#day2 = day("04.20.2007")
#dayandrew = day("09.28.1989", startOfDay="0145", endOfDay="2400")
#dayjohn = day("06.29.1992", startOfDay="0550")
#dayroy = day("12.01.1947")
#daymarleen = day("04.15.1957")

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


