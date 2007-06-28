import urllib, urlparse, gzip
import datetime
import nuclasses
from StringIO import StringIO
from xml.dom import minidom

USER_AGENT = 'Tote/0.1 +http://tote.chatonka.com/' #Not in use yet


def zoho_list_item_to_tote_task(item):
    print item
    listID = item[0]
    listName = item[1]
    subItems = item[2]
    tote_task_item = nuclasses.task(listName, zohoID=listID)
    for each in subItems:
        listID = each[0]
        listName = each[1]
        nuclasses.task(listName, zohoID=listID, parentTask=tote_task_item)
    return tote_task_item
    
        


class ZohoAccount:
    def __init__(self):
        self.API_KEY="635ea1a7ddff850c5b7301b33ea3a944" #This is for Tote ONLY
        self.ALL_PAGES_XML="http://planner.zoho.com/api/private/xml/pages"
        self.ALL_LISTS_XML="http://planner.zoho.com/api/private/xml/lists"
        #Temporary Things
        self.login_id = "wolf08"
        self.password = "priorlake"
        self.current_ticket = None
        self.known_pages = {} #Format of {'id_number', 'page_title'}
        self.current_home_page = None
        
    def get_ticket(self):
        if not self.current_ticket:
            return self.login(self.login_id, self.password)
        else:
            return self.current_ticket

    def add_known_page(self, pageID, pageTitle):
        for id in self.known_pages:
            if id == pageID:
                return (id, self.known_pages[id]) #Return (id, title)
                nuclasses.log_info("found page with id %s" % id)
            else:
                pass
        nuclasses.log_info("Didn't find any previous page with id number %s" % pageID)
        self.known_pages[pageID] = pageTitle
    
    def parse_login_response(self, response):
        #Do some stuff here and return either they key or None
        response_rows = response.split("\n")
        for entry in response_rows:
                entry = entry.split("=")
                if entry[0] == "RESULT":
                    if entry[1] == "FALSE":
                        return None #This means we didn't log in correctly, so we return so
                elif entry[0] == "TICKET":
                    return entry[1]
        nuclasses.log_error("Unable to determine ticket... Here is our debug output:\n%s" % response_rows)
        return None
    
    def get_pages(self):
        ticket = self.get_ticket()
        pages_unformatted_xml = urllib.urlopen(self.ALL_PAGES_XML + "?ticket=%s&apikey=%s" % (ticket, self.API_KEY)).read()
        pages_xml = minidom.parseString(pages_unformatted_xml)
        nuclasses.log_info(pages_xml.toxml())
        list_of_page_details = pages_xml.firstChild.firstChild.firstChild.childNodes
        for each in list_of_page_details:
            current_page = each
            pageID = current_page.childNodes[0].firstChild.data
            pageTitle = current_page.childNodes[1].firstChild.data 
            if current_page.childNodes[2].firstChild.data == "true":
                self.current_home_page = pageID
            self.add_known_page(pageID, pageTitle)
        return self.known_pages
           
    def reset_pages(self):
        self.known_pages = {}
        return self.get_pages()
            
    def get_lists_on_page(self, pageID):
        ticket = self.get_ticket()
        lists_unformatted_xml = urllib.urlopen(self.ALL_LISTS_XML + "?ticket=%s&apikey=%s&pageId=%s" % (ticket, self.API_KEY, pageID)).read()
        lists_xml = minidom.parseString(lists_unformatted_xml)
        nuclasses.log_info(lists_xml.toxml())
        lists_details = lists_xml.firstChild.firstChild.firstChild.lastChild.childNodes
        lists_on_page = []
        for each in lists_details:
            listID = each.firstChild.firstChild.data
            listName = each.childNodes[1].firstChild.data
            try:
                items = []
                unit = each.childNodes[2]
                while unit.nextSibling != None:
                    items.append(unit)
                    unit = unit.nextSibling
            except IndexError:
                nuclasses.log_info("List '%s' has no subItems." % listName)
                items = []
            lists_on_page.append([listID, listName, items])
        return lists_on_page
        
    def xml_subItems_to_lists(self, item):
        print item
        subItemsList = []
        for each in item[2]:
            id = each.childNodes[0].firstChild.data
            name = each.childNodes[1].firstChild.data
            subItemsList.append([id, name, []])
        return [item[0], item[1], subItemsList]
    
    def login(self, login_id, password):
        urlstring = "https://accounts.zoho.com/login?servicename=ZohoPlanner&silent=true&LOGIN_ID=%s&PASSWORD=%s&FROM_AGENT=true" %(login_id, password)
        response = urllib.urlopen(urlstring).read()
        ticket = self.parse_login_response(response)
        if ticket:
            self.current_ticket = ticket
            return ticket
        else:
            nuclasses.log_error("No ticket!")
            
andrew = ZohoAccount()
andrew.get_pages()
a = andrew.get_lists_on_page("81351")
print "A is: ", a
b = andrew.xml_subItems_to_lists(a[0])
print "B is: ", b
c = zoho_list_item_to_tote_task(andrew.xml_subItems_to_lists(andrew.get_lists_on_page("81351")[0]))
print "C is: ", c

            
            
# 99bf6d6c4e24e7b23e02fc5e2f375559
            