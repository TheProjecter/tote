#dayofweek is an int (0-6, sun-sat)
#schedule is wtf happens on this day (schedules are their own class, 
#                                        numbered by integer for each profile

class user:
    def __init__(self, name):
        self.name = name
        
    def addEvent(self):
        pass
    def addTask(self):
        pass
    def add(self?):
        pass

class day:
    def __init__(self, dayofweek, schedule=-1):
        self.dayofweek = dayofweek
        if schedule == -1:
            self.schedule = dayofweek
        else:
            self.schedule = schedule
        self.known = 1
        
        
        

        
#dailyActivities is a list that includes activities. Activities can be blocks, things, or
class schedule:
    def __init__(self, dailyActivities, transitTimes):
        self.dailyActivities = dailyActivities
        self.transitTimes = transitTimes

#eventTypes are objects that fundamentally occur at ta time.
#They can be permenant (blocks) or semiperminant (things).
#Both have the same ways of accessing their data

eventTypes = ["block", "thing"]

#className is a hr string
#blockLayout is: when is this block (days, time of day)
#meetsOnDays is a list of numbers (0,6 for sun-sat)
class block:
    def __init__(self, blockNumber, className, blockLayout, meetsOnDays):
        self.blockNumber = blockNumber
        self.className = className
        self.blockLayout = blockLayout
        self.meetsOnDays = meetsOnDays

##A 'thing' is like a tempoary block. It returns the same type of info as a block,
## and therefore can be used in place of a block. However, they are initialized differently!
# repeated is an int. does this thing reoccur?  
#startTime and endTime are given as unix time format       
class thing:
    def __init__(self, repeated=0, startTime, endTime):
        self.oneUse = oneUse
        self.startTime = startTime
        self.endTime = endTime
        
        
        
#Classes related to tasks. These have startDates and dueDates to differentiate
#from the startTimes and endTimes of blocks and things.
taskTypes = ["assignment", "project"]

class assignment:
    def __init__(self, startDate, dueDate, description="", parentEvents=[], resources=[]):
        #common to tasks
        self.startDate = startDate
        self.dueDate = dueDate
        self.relatedTasks = []
        self.resources = []
        self.description = description
        self.progress = 0
        for each in relatedTasks:
            self.relatedTasks.append(each)
        for each in resources:
            self.resources.append(each)
        
        #assignment only
        self.parentEvents = []
        for each in parentEvents:
            self.parentEvents.append(each)

    #common to tasks
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
        
    #assignments Only            
    def assignToEvent(self, event): #The event handle
        return self.parentEvents.append(event)
        
    def removeFromEvent(self, event): #event handle
        try:
            return self.parentEvents.remove(event)
        except ValueError:
            return 0            
        
class project:
    def __init__(self, startDate, dueDate):
        #common to tasks
        self.startDate = startDate
        self.dueDate = dueDate
        self.relatedTasks = []
        self.resources = []
        self.description = description
        self.progress = 0
        for each in relatedTasks:
            self.relatedTasks.append(each)
        for each in resources:
            self.resources.append(each)

        #Unique to Projects
        self.assignments = []
        self.parentEvents = []
        
    def addAssignment(self, assignment):
        self.assignments.append(assignment)
        
    def addDescription(self, description): #description is a str
        self.description = description
        
    def assignToEvent(self, event): #The event handle
        self.parentEvents.append(event)
        
    def removeFromEvent(self, event): #event handle
        self.parentEvents.remove(event)

    def duration(self):
        import time
        return pseudo: end - start
        
        