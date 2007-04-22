import pickle
import objects

def noComprendo(your_input):
    return "\nWhat? I can't understand '%s'...\n" % your_input


def getDate(): #In date format
    import time
    localdate = str(time.localtime()[0:3])[1:-1].split(', ') #List: (year(xxxx), month(1-12), day(1-31))
    if int(localdate[1]) < 10: #Making sure the month is 2 digets, eg 01 instead of 1
        localdate[1] = str('0%s' % localdate[1])
    else:
        pass
    
    if int(localdate[2]) < 10: #Doing the same for the day
        localdate[2] = str('0%s' % localdate[2])
    else:
        pass
    return localdate


def loadTasks(taskFile):
    try:
        dataFile = open(taskFile, 'r')
    except IOError:
        dataFile = open(taskFile, 'w+r')
    #newData = dataFile.readlines()
    #for each in newData: # Time to unpickle!
    #    print newData[newData.index(each)]
    #    newData[newData.index(each)] = pickle.loads[each]
    newData = []    
    while 1:
        try:
            newData.append(pickle.load(dataFile))
        except EOFError:
            break
    dataFile.close
    return newData


def storeTasks(taskFile, openTasks):
    dataFile = open(taskFile, 'w')
    for each in openTasks:
        pickle.dump(each, dataFile)    #Pickling....
#        dataFile.write("%s\n" % each)
    return 1

def removeTask(openTasks, task):
    openTasks.pop(openTasks.index(task))
    return openTasks

def addTask(hrName, Class, dueDate=-1, assignDate=-1, priority=-1, description="", longTerm=0):
    tempTask = objects.Assignment(hrName, Class, dueDate, assignDate, priority, description, longTerm)
    #why have this function?...
    return tempTask

def tasksForTomorrow(taskList):
    tasksDueTomorrow = []
    tomorrowdate = getDate()
    tomorrowdate[2] = str(int(tomorrowdate[2]) + 1) #Make it tomorrow
    tomorrowdate = ''.join(tomorrowdate) #Join them together (yyyymmdd)
    for each in range(len(taskList)):
        try:
            if taskList[each].dueDate == tomorrowdate:
                tasksDueTomorrow.append(taskList[each])
        except IOError:
            pass
    return tasksDueTomorrow

def tasksForDate(taskList, date):
    tasksDueOnDate = []
    for each in range(len(taskList)):
        try:
            if str(taskList[each].dueDate) == str(date):
                tasksDueOnDate.append(taskList[each])
        except IOError:
            pass
    return tasksDueOnDate
