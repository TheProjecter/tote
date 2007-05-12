import vobject

class iCal:
    pass





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