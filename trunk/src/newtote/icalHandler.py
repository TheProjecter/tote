import vobject
import datetime
import nuclasses
import itertools
import StringIO
defaultFolderStructure = [
                            "./data",
                            "./data/default",
                            "./config"]
    
defaultFileStructure = [
                        "./data/default/defaultEventCalendar.ics",
                        "./data/default/defaultTaskCalendar.ics",
                        "./config/default/defaultConfig.conf"]
ICS_STOCK_EVENTS = defaultFileStructure[0]
ICS_STOCK_TASKS = defaultFileStructure[1]



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
# A complete implementation of current DST rules for major US time zones.

def first_sunday_on_or_after(dt):
    days_to_go = 6 - dt.weekday()
    if days_to_go:
        dt += timedelta(days_to_go)
    return dt

# In the US, DST starts at 2am (standard time) on the first Sunday in April.
DSTSTART = datetime.datetime(1, 4, 1, 2)
# and ends at 2am (DST time; 1am standard time) on the last Sunday of Oct.
# which is the first Sunday on or after Oct 25.
DSTEND = datetime.datetime(1, 10, 25, 1)

class USTimeZone(datetime.tzinfo):

    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = datetime.timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            # An exception may be sensible here, in one or both cases.
            # It depends on how you want to treat them.  The default
            # fromutc() implementation (called by the default astimezone()
            # implementation) passes a datetime with dt.tzinfo is self.
            return ZERO
        assert dt.tzinfo is self

        # Find first Sunday in April & the last in October.
        start = first_sunday_on_or_after(DSTSTART.replace(year=dt.year))
        end = first_sunday_on_or_after(DSTEND.replace(year=dt.year))

        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        if start <= dt.replace(tzinfo=None) < end:
            return HOUR
        else:
            return ZERO

Eastern  = USTimeZone(-5, "Eastern",  "EST", "EDT")
Central  = USTimeZone(-6, "Central",  "CST", "CDT")
Mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
Pacific  = USTimeZone(-8, "Pacific",  "PST", "PDT")




class Session:
    def __init__(self, dataFiles=defaultFileStructure, configFile=0):
        self.icals = {ICS_STOCK_EVENTS: vobject.iCalendar(), ICS_STOCK_TASKS: vobject.iCalendar()}
        self.dataFiles=dataFiles
    
    def addiCal(self, ical, path):
        path = os.path.expanduser(path)
        self.ical[path] = ical


def exportEventsToiCal(list_of_events, ical):
    for event in list_of_events:
        eventToiCal(event, ical)
def exportiCalToFile(ical, file, overwrite):
    if not overwrite:
        pass
    else:
        s = ical.serialize()
        f = open(file, "w")
        f.write(s)
        f.close()
        
def importiCalFromFile(file):
    f = open(file, "r")
    dataAsList = f.readlines()
    print dataAsList
    data = ""
    for each in dataAsList:
        data = data + each
    print data
    (dict, other) = itemsFromVObject(data)
    return dict
        


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
                
#def eventToiCal(event, ical):
    #ical.add('vevent')
    #ical.vevent.add('summary').value = event.name
    #ical.vevent.add('description').value = event.description
    #ical.vevent.add('')
    #icalstart = ical.vevent.add('dtstart')
    #print icalstart
    #ical.prettyPrint()
    
def taskToiCal(task, ical):
    ical.add('vevent')
    ical.vevent.add('summary').value = task.name
    ical.vevent.add('description').value = task.description
    #ical.vevent.add('')
    task.dtstart = ical.vevent.add('dtstart')
    

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


#eventToiCal(ical, nuclasses.events[2])


def tasksToVObject(tasks, cal=None):
    """
    Iterate through items, add to cal, create a new vcalendar if needed.
    """
    
    def populate(comp, task):
        """Populate the given vobject vevent with data from item."""
        comp.add('summary').value = task.name
        
        try:
            dtstartLine = comp.add('dtstart')
            dtstartLine.value = task.dateTime
            
        except AttributeError:
            comp.dtstart = [] # delete the dtstart that was added
            
        try:
            dtendLine = comp.add('dtend')
            dtendLine.value = task.endTime
        
        except AttributeError:
            comp.dtend = [] # delete the dtend that was added

            
        try:
            comp.add('description').value = task.description
        except AttributeError:
            pass
        
        try:
            comp.add('location').value = item.location.displayName
        except AttributeError:
            pass        

        #End of populate
        
    if cal is None:
        cal = vobject.iCalendar()
    for task in tasks:
            try:
                populate(cal.add('vevent'), task)
            
            except:
                continue
    cal.prettyPrint()
            
    return cal


def itemsFromVObject(serializedcalobject=None):
    #if vobject == None:
        
    countNew = 0
    countUpdated = 0

    itemlist = []

    calname = None
    text = serializedcalobject
    print text
    # iterate over calendars, usually only one, but more are allowed
    for calendar in vobject.readComponents(text, validate=True):
        modificationQueue = []
        calendar.prettyPrint()
        # just grab the first calendar name
        if calname is None:
            calname = calendar.getChildValue('x_wr_calname')

        rawVevents = getattr(calendar, 'vevent_list', [])
        numVevents = len(rawVevents)
        #if updateCallback and monolithic:
        #    updateCallback(msg=_(u"Calendar contains %d events") % numVevents,
        #        totalWork=numVevents)

        vevents = ((-1, event) for event in rawVevents)
        for i, event in itertools.chain(vevents, enumerate(modificationQueue)):
            # Queue modifications to recurring events so modifications are
            # processed after master events in the iCalendar stream.
            recurrenceID = event.getChildValue('recurrence_id')
            if recurrenceID is not None and i < 0:
                # only add to modificationQueue in initial processing
                modificationQueue.append(event)
                continue

            try:
                #if DEBUG: logger.debug("got VEVENT")
                #pickKind = eventKind

                name        = event.getChildValue('summary', u"")
                description = event.getChildValue('description')
                location    = event.getChildValue('location')
                status      = event.getChildValue('status', "").lower()
                duration    = event.getChildValue('duration')
                dtstart     = event.getChildValue('dtstart')
                dtend       = event.getChildValue('dtend')
                due         = event.getChildValue('due')
                uid         = event.getChildValue('uid')

                """
                if status in ('confirmed', 'tentative'):
                    pass
                elif status == 'cancelled': #Chandler doesn't have CANCELLED
                    status = 'fyi'
                else:
                    status = 'confirmed'

                isDate = type(dtstart) == date

                # RFC2445 allows VEVENTs without DTSTART, but it's hard to guess
                # what that would mean, so we won't catch an exception if there's no
                # dtstart.
                anyTime = getattr(event.dtstart, 'x_osaf_anytime_param', None) == 'TRUE'

                try:
                    reminderDelta = event.valarm.trigger.value
                    if type(reminderDelta) is datetime.datetime:
                        reminderDelta = reminderDelta - dtstart
                except AttributeError:
                    reminderDelta = None

                """
                if duration is None:
                    if dtend is not None:
                        duration = dtend - dtstart
                    elif due is not None: #VTODO case
                        duration = due - dtstart
#                    elif anyTime or isDate:
#                        duration = oneDay
                    else:
                        duration = datetime.timedelta(0)


#                if isDate:
#                    dtstart = TimeZone.forceToDateTime(dtstart)
                    # convert to Chandler's notion of all day duration
#                    duration -= oneDay

                # coerce timezones based on coerceTzinfo

#                if coerceTzinfo is not None:
#                    dtstart = TimeZone.coerceTimeZone(dtstart, coerceTzinfo)

#                dtstart = convertToICUtzinfo(dtstart, view)
                # Because of restrictions on dateutil.rrule, we're going
                # to have to make sure all the datetimes we create have
                # the same naivete as dtstart
                tzinfo = dtstart.tzinfo

                # by default, we'll create a new item, not change existing items
                itemChangeCallback = None
                """
                # See if we have a corresponding item already
                uidMatchItem = Calendar.findUID(view, uid)

                if uidMatchItem is not None:
                    #if DEBUG: logger.debug("matched UID")

                    if recurrenceID:
                        if type(recurrenceID) == date:
                            recurrenceID = datetime.datetime.combine(
                                                        recurrenceID,
                                                        time(tzinfo=tzinfo))
                        else:
                            recurrenceID = convertToICUtzinfo(
                                               makeNaiveteMatch(recurrenceID,
                                               tzinfo), view)

                        eventItem = uidMatchItem.getRecurrenceID(recurrenceID)
                        if eventItem == None:
                            # our recurrenceID didn't match an item we know
                            # about.  This may be because the item is created
                            # by a later modification, a case we're not dealing
                            # with.  For now, just skip it.
                            logger.info("RECURRENCE-ID didn't match rule. " \
                                        "RECURRENCE-ID = %s" % recurrenceID)
                            continue
                        recurrenceLine = event.contents['recurrence-id'][0]
                        range = recurrenceLine.params.get('RANGE', ['THIS'])[0]
                        if range == 'THISANDPRIOR':
                            # ignore THISANDPRIOR changes for now
                            logger.info("RECURRENCE-ID RANGE of THISANDPRIOR " \
                                        "not supported")
                            continue
                        elif range == 'THIS':
                            itemChangeCallback = CalendarEventMixin.changeThis
                            # check if this is a modification to a master event
                            # if so, avoid changing the master's UUID when
                            # creating a modification
                            if eventItem.getMaster() == eventItem:
                                mod = eventItem._cloneEvent()
                                mod.modificationFor = mod.occurrenceFor = eventItem
                                if eventItem.hasLocalAttributeValue('occurrenceFor'):
                                    del eventItem.occurrenceFor
                                eventItem = mod
                        elif range == 'THISANDFUTURE':
                            itemChangeCallback = CalendarEventMixin.changeThisAndFuture
                        else:
                            logger.info("RECURRENCE-ID RANGE not recognized. " \
                                        "RANGE = %s" % range)
                            continue

                    else:
                        eventItem = uidMatchItem
                        if (eventItem.occurrenceFor is None and
                            eventItem.occurrences is None):
                                eventItem.occurrenceFor = eventItem
                        if eventItem.rruleset is not None:
                            # re-creating a recurring item from scratch, delete
                            # old recurrence information
                            # uidMatchItem might not be the master, though, so
                            # get the master, or eventItem will be a deleted
                            # event
                            eventItem = eventItem.getMaster()
                            # delete modifications the master has, to avoid
                            # changing the master to a modification with a
                            # different UUID
                            if getattr(eventItem, 'modifications', None):
                                for mod in eventItem.modifications:
                                    mod.delete()
                            eventItem.removeRecurrence()

                        itemChangeCallback = CalendarEventMixin.changeThis
                        countUpdated += 1
                    if DEBUG: logger.debug("Changing eventItem: %s" % str(eventItem))
                """
                changesDict = {}
                change = changesDict.__setitem__

                change('name', name)

#                if anyTime:
#                    change('anyTime', True)
#                    change('allDay', False)
#                elif isDate:
                    # allDay events should have anyTime True, so if the user
                    # unselects allDay, the time isn't set to midnight
#                    change('anyTime', True)
#                    change('allDay', True)
#                else:
#                    change('allDay', False)
#                    change('anyTime', False)

                change('startTime', dtstart)
                change('duration', duration)
                change('endTime', dtend)

#                if not filters or "transparency" not in filters:
#                    change('transparency', status)

                # DESCRIPTION <-> body
                if description is not None:
                    change('description', description)

#                if location:
#                    change('location', Calendar.Location.getLocation(view,
#                                                                     location))

                # rruleset and reminderInterval need to be set last
                """
                changeLast = []
                if not filters or "reminders" not in filters:
                    if reminderDelta is not None:
                        changeLast.append(('reminderInterval', reminderDelta))

                rruleset = event.rruleset
                if rruleset is not None:
                    ruleSetItem = RecurrenceRuleSet(None, itsView=view)
                    ruleSetItem.setRuleFromDateUtil(rruleset)
                    changeLast.append(('rruleset', ruleSetItem))

                if itemChangeCallback is None:
                    # create a new item
                    # setting icalUID in the constructor doesn't seem to work
                    #change('icalUID', uid)
                    eventItem = pickKind.newItem(None, newItemParent, **changesDict)
                    # set icalUID seperately to make sure uid_map gets set
                    # @@@MOR Needed anymore since we got rid of uid_map?
                    eventItem.icalUID = uid
                    for tup in changeLast:
                        eventItem.changeThis(*tup)
                    countNew += 1
                else:
                    # update an existing item
                    if rruleset is None and recurrenceID is None \
                       and eventItem.rruleset is not None:
                        # no recurrenceId or rruleset, but the existing item
                        # may have recurrence, so delete it
                        eventItem.removeRecurrence()

                    for attr, val in changesDict.iteritems():

                        # Only change a datetime if it's really different
                        # from what the item already has:
                        if type(val) is datetime.datetime and hasattr(eventItem,
                            attr):
                            oldValue = getattr(eventItem, attr)
                            if (oldValue == val and
                                oldValue.tzinfo == val.tzinfo):
                                continue

                        itemChangeCallback(eventItem, attr, val)


                    for (attr, val) in changeLast:
                        itemChangeCallback(eventItem, attr, val)



                if DEBUG: logger.debug(u"Imported %s %s" % (eventItem.displayName,
                 eventItem.startTime))

                if updateCallback:
                    msg="'%s'" % eventItem.getItemDisplayName()
                    # the work parameter tells the callback whether progress
                    # should be tracked, this only makes sense if we might have
                    # more than one event.
                    cancelled = updateCallback(msg=msg, work=monolithic)
                    if cancelled:
                        raise Sharing.SharingError(_(u"Cancelled by user"))
                """
                # finished creating the item
                print changesDict
                itemlist.append(changesDict)

    
            #except Sharing.SharingError:
            #    raise

            except Exception, e:
                if __debug__:
                    raise
                else:
                    logger.exception("import failed to import one event with \
                                     exception: %s" % str(e))

    else:
        # an empty ics file, what to do?
        pass

    #logger.info("...iCalendar import of %d new items, %d updated" % \
    # (countNew, countUpdated))

    return itemlist, calname


def addTasksFromCalDict(itemlist):
    for t in itemlist:
        nuclasses.task(t["name"], description=t["description"], startTime=t["startTime"])
