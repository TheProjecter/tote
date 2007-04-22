import Base.functions as gf
import Base.objects
import os
import time
from conf import configInit

#Common Variables (Please don't set this to an absolute path unless you know what you're doing)

# classList = ["Spanish 5", "Calc AB", "Choir", "AP Chem", "Acc Physics", "Free Block", "English"]
def pause():
    raw_input("\nPress enter to continue")
    
header = """VSTMS: Very Simple Task Menu System
In other words, the text version of
    
    Tote - Manage your life"""
taskParts = ["self", "hrName", "Class", "dueDate", "assignDate", "priority", "description", "longTerm"]
classList = configInit.grab_class_config()
print classList


gv = Base.objects.variables()

gv.openTasks = []
gv.classList = classList
#gv.taskFile = taskFile
gv.taskParts = taskParts

print header
while 1:
 try:
    print """
What would you like to do?

1. View Outstanding Tasks
2. View Tasks due...
3. Add New Task
4. Delete Task
5. Save Tasks
6. Reload Tasks
0. Exit
"""
    choice = input("Please enter a number, 1-6 (or 0):   ")
    if choice == 1:
        print "\nOutstanding Tasks:"
        for each in gv.openTasks:    
            print "     %s from %s, assigned on %s" % (each.hrName, gv.classList[int(each.Class) - 1], each.assignDate)
            
        pause()
    if choice == 2:
        while 1:
            try:
                choice_date = raw_input("Give me a date (yyyymmdd)! Enter 1 for tomorrow, 0 to go back:  ")
                if int(choice_date) == 1:
                    tomorrowTasks = gf.tasksForTomorrow(gv.openTasks)
                    print "Tasks Due Tomorrow:"
                    for each in tomorrowTasks:    
                        print "     %s from %s, assigned on %s" % (each.hrName, gv.classList[int(each.Class) - 1], each.assignDate)
                elif int(choice_date) == 0:
                    break            
                else:
                    dateTasks = gf.tasksForDate(gv.openTasks, int(choice_date))
                    print "Tasks Due on %s:" % choice_date
                    for each in dateTasks:    
                        print "     %s from %s, assigned on %s" % (each.hrName, gv.classList[int(each.Class) - 1], each.assignDate)
            except ValueError:
                print "Please... Give me a __DATE__, not something else!"            
    if choice == 3:
        #This isn't done yet, but oh well...
        print "\nOk... Watch Carefully:\n"
        print "You need to enter the colums that are starred\n"
        print "*Name, *Class Number, Due Date, Date Assigned, Priority, Description, LongTerm(bool)"
        #dueDate = -1
        #assignDate = -1
        #priority = -1
        #description = ""
        #longTerm = 0
        hrName = raw_input("Name:  ")
        Class = raw_input("Class Number:  ")
        dueDate = raw_input("Date Due:  ")
        assignDate = raw_input("Date Assigned:  ")
        priority = raw_input("Priority:  ")
        description = raw_input("Description (String!):  ")
        longTerm = input("Long Term? (bool):  ")
        #Put this next bit into a module?
        toCheck = [dueDate, assignDate, priority]
        for each in toCheck:
            if each == "":
                each = -1
            else:
                try:
                    if int(each):
                        print "Value ok"
                except TypeError:
                    print "Changing to -1"
                    each = -1
        
        gv.openTasks.append(gf.addTask(hrName, Class, dueDate, assignDate, priority, description, longTerm))
    if choice == 4:
        pass
    if choice == 5:
        if gf.storeTasks(gv.taskFile, gv.openTasks):
            print "Save Successful"
        else:
            print "Hmm, something went wrong... Yuck! I hope you weren't using this on a production system!"        
    if choice == 6:
        while 1:
            choice_goahead = raw_input("Are you sure you want to do this? It overwrites non-saved tasks! (y/n):  ")
            if choice_goahead == "y":
                print "\n Okay! Reloading....\n"
                gv.openTasks = gf.loadTasks(gv.taskFile)
                break
            elif choice_goahead == "n":
                print "\nGot it! I won't reload\n"
                break
            else:
                print gf.noComprendo(choice_goahead)
    if choice == 0:
        while 1:
            choice_save = raw_input("Exiting... Do you wish to save? (y/n):  ")
            if choice_save == "y":
                if gf.storeTasks(gv.taskFile, gv.openTasks):
                    print "Save Successful"
                else:
                    print "Hmm, something went wrong... Yuck! I hope you weren't using this on a production system!"
                break
            elif choice_save == "n":
                break
            else:
                print gf.noComprendo(choice_save)
        break
    print "---------------------------------------------------------\n\n"
 except NameError:
    print "Bleh! Give me a number!"
    pause()
 except SyntaxError:
    print "I need a response....!"
    pause()