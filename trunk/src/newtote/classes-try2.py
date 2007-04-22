days = []
tomorrows = [none]


def convertToSeconds(hours=0, days=0, weeks=0, years=0):
    pass

def addTime(currentTime, seconds=0):
    import time
    return time.localtime(time.mktime(currentTime) + seconds)
    
def timeToDay(tempTime):
    import time
    dateWanted = tempTime[1] + tempTime[2]
    for each in days:
        print each.date, dateWanted
        if each.date == dateWanted:
            day = each
        else:
            pass
    
    
    
        
    
    
    
def updateDate(date=-1):
    import time
    if date=-1
        date = []
        for each in time.localtime():
          date.append(each)
    if tomorrows[0]. == 
    


class day:
    def __init__(self, startOfDay=0600, endOfDay=2000, date): #ie 1124
        self.startOfDay = startOfDay
        self.endOfDay = endOfDay
        self.date = date
        days.append(self)
        
        
        
        

class task:
    def __init__(self, startDate=-1, dueDate=-1, description="", parentEvents=[], resources=[], relatedTasks=[], isProject=0):
        #Setting the dates
        import time
        if startDate == -1:
            startDate = time.localtime()
        else:
            try:
                print "Start Date is: ", time.asctime(startDate)
                self.startDate = startDate
            except TypeError:
                startDate = time.localtime()
        if dueDate == -1:
            dueDate = addTime(time.localtime(), 86400)
        else:
            
            ############## working on date here. Start of day? End of day? ###################
            try:
                print "Due Date is: ", time.asctime(dueDate)
                self.dueDate = dueDate
            except TypeError:
                dueDate = time.localtime()
        self.dueDate = dueDate
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
            


    def assignRelatedTask(self, task):
        return self.relatedTasks.append(task)
        
    def removeRelatedTask(self, task):
        try:
            return self.relatedTasks.remove(task)
        except ValueError:
            return 0

    def assignResource(self, resource):
        return self.resources.append(resource)
        
    def removeResource(self, resource):
        try:
            return self.resources.remove(resource)
        except ValueError:
            return 0
        

    def assignToEvent(self, event): #The event handle
        return self.parentEvents.append(event)
        
    def removeFromEvent(self, event): #event handle
        try:
            return self.parentEvents.remove(event)
        except ValueError:
            return 0            
                
    def addSubTask(self, task):
        self.subTasks.append(task)
        
    desc = []
        
    def Adddescription(self, description): #description is a str
        self.description = description

    def duration(self):
        import time
        #return pseudo: end - start
        
a = task(123, 435)

def timeBetweenEvents(event1, event2):
    if event1.startDate < event2.startDate:
        firstInTime = event1
    else:
        firstInTime = event2
        
    