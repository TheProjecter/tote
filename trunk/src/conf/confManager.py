#!/usr/bin/env python
import ConfigParser
import os

# Conf file
# Please do not change this unless you know what you are doing
confFiles = ['/etc/tote/tote.conf', os.path.expanduser('~/.tote.conf')]


class config:
    def __init__(self, defaultFile=os.path.expanduser('~/.tote/tote.defaults.conf'), confFiles=confFiles):
        self.confFile = confFiles
        print os.getcwd()
        self.confParser = ConfigParser.SafeConfigParser()
        try:
            self.confParser.readfp(open(defaultFile))
        except IOError:
            try:
                tempFile = open(defaultFile, "w")
            except IOError:
                os.mkdir(os.path.expanduser('~/.tote/'))
                tempFile = open(defaultFile, "w")
            tempFile.write("""# This is the default configuration file for Tote
# Locations and other config options are listed in here
# Please, do not change this data unless you know exactly what you are doing
# In most cases, ~/.tote.conf works fine.

[Files]
taskFile = ~/.tote/tasks.dat
classesFile = ~/.tote/classes.dat

[Classes]
number_of_classes = 7
1 = Spanish 5
2 = Calc AB
3 = Choir
4 = AP Chem
5 = Acc Physics
6 = Free Block
7 = English

""")
            tempFile.close()
            self.confParser.readfp(open(defaultFile))
        self.filesParsed = self.confParser.read(confFiles)
    
    def add_config(self, section, values): #Values is given as a dict, section as a str
        if self.confParser.has_section(section):
            pass
        else:
            self.conParser.add_section(section)
        for key in values.keys():
            self.confParser.set(section, key, values[key])
        
    def write_config(self):
        tempFile = open(os.path.expanduser('~/.tote.conf'), "w")
        self.confParser.write(tempFile)
        tempFile.close()
        
    def reload_config(self):
        self.confParser.readfp(open(os.path.expanduser('~/.tote/tote.defaults.conf')))
        self.filesParsed = self.confParser.read(confFiles)
        return self.filesParsed
    
    def del_config(self, section, option):
        try:
            return self.confParser.remove_option(section, option)
        except NoSectionError:
            return "NoSectionError"
        
    def del_section(self, section):
        return self.confParser.remove_section(section)
    
    def get_option(self, section, option):
        return self.confParser.get(section, option)
    
    