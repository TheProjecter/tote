import time
import os

def add_task():
    print "Please describe your task:"
    name = raw_input("Name:  ")
    print "The rest of these questions are optional. Default values are in ()"
    description = raw_input("Discribe this task: (None) ")
    assignDate = raw_input("When was it assigned? (%s) " % os.popen("""date +"%a %b %d, %Y %H:%M" """).read()[:-1:])
    dueDate = raw_input("When is it due? (tomorrow, same time) ")
    print name, description, assignDate, dueDate
    
    
add_task()