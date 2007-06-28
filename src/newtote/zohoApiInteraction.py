import urllib, urlparse, gzip
import datetime
import nuclasses
from StringIO import StringIO
from xml.dom import minidom

USER_AGENT = 'Tote/0.1 +http://tote.chatonka.com/' #Not in use yet


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
        if not self.current_ticket:
            ticket = self.login(self.login_id, self.password)
        else:
            ticket = self.current_ticket
        response = urllib.urlopen(self.ALL_PAGES_XML + "?ticket=%s&apikey=%s" % (ticket, self.API_KEY))
        pages_unformatted_xml = response.read()
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
        print self.known_pages
        print self.current_home_page
        print self.known_pages[self.current_home_page]
            
    
        
    
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
            
            
# 99bf6d6c4e24e7b23e02fc5e2f375559
            