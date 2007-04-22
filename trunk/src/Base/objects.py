#!/usr/bin/python
import functions as gf

class variables:    #This is actually short for GlobalVarables
    pass

class Assignment:
    def __init__(self, hrName, Class, dueDate=-1, assignDate=-1, priority=-1, description="", longTerm=0):
        self.hrName = hrName
        self.Class = Class
        if dueDate == -1: #Set due date to tomorrow
            localdate = gf.getDate()
            localdate[2] = str(int(localdate[2]) + 1)    
            self.dueDate = ''.join(localdate)

        else:
            self.dueDate = dueDate 
            #This assumes that the dueDate is given in proper format (yyyymmdd)
        #Now we get to do the same thing for the assignment date:
        if assignDate == -1: #Set due date to tomorrow
            localdate = gf.getDate()
            self.assignDate = ''.join(localdate)
        else:
            self.assignDate = assignDate 
            #This assumes that the assig`nDate is given in proper format (yyyymmdd)
            self.priority = priority
            self.description = description
            self.longTerm = longTerm
            self.deps = []
            self.media = []
    def addDep(self, dep):
        self.deps.append(dep)

    def viewDeps(self, attr):
        for each in self.deps:
            pass
                
            
    def addMedia(self, media):
        self.media.append(media)

        
class Category:
    def __init__(self, hrName):
        self.hrName = hrName
        

class Class:
    def __init__(self, hrName, block, teacher):
        self.hrName = hrName
        self.block = block
        self.teacher = teacher
    
    def __name__(self):
        return self.hrName
