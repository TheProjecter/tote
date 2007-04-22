#!/usr/bin/env python

import gobject
import gtk
import nuclasses
import time

(
  COLOR_RED,
  COLOR_GREEN,
  COLOR_BLUE
) = range(3)

(
  SHAPE_SQUARE,
  SHAPE_RECTANGLE,
  SHAPE_OVAL,
) = range(3)

(
    COLUMN_TASKS_COMPLETED,
    COLUMN_TASKS_NAME,
    COLUMN_TASKS_DUE,
    COLUMN_TASKS_DESCRIPTION
) = range(4)

(
    COLUMN_BOTH_COMPLETED,
    COLUMN_BOTH_NAME,
    COLUMN_BOTH_TYPE,
    COLUMN_BOTH_DATE,
    COLUMN_BOTH_DESCRIPTION,
    COLUMN_BOTH_RELATED
) = range(6)
 
(
    OPTION_ADD_TASK,
    OPTION_ADD_EVENT
) = range(2)


ui_info = \
'''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menu action='NewMenu'>
       <menuitem action='Task'/>
       <menuitem action='Event'/>
       <separator/>
       <menuitem action='Project'/>
       <menuitem action='Block'/>
       <separator/>
       <menuitem action='Resource'/>
      </menu>
      <menuitem action='Open'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='PreferencesMenu'>
      <menu action='ColorMenu'>
        <menuitem action='Red'/>
        <menuitem action='Green'/>
        <menuitem action='Blue'/>
      </menu>
      <menu action='ShapeMenu'>
        <menuitem action='Square'/>
        <menuitem action='Rectangle'/>
        <menuitem action='Oval'/>
      </menu>
      <menuitem action='Bold'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar  name='ToolBar'>
    <toolitem action='Open'/>
    <toolitem action='Quit'/>
    <separator/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>'''



# It's totally optional to do this, you could just manually insert icons
# and have them not be themeable, especially if you never expect people
# to theme your app.
def register_stock_icons():
    ''' This function registers our custom toolbar icons, so they
        can be themed.
    '''
    items = [('demo-gtk-logo', '_GTK!', 0, 0, '')]
    # Register our stock items
    gtk.stock_add(items)

    # Add our custom icon factory to the list of defaults
    factory = gtk.IconFactory()
    factory.add_default()

    import os
    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)

        # Register icon to accompany stock item

        # The gtk-logo-rgb icon has a white background, make it transparent
        # the call is wrapped to (gboolean, guchar, guchar, guchar)
        transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
        icon_set = gtk.IconSet(transparent)
        factory.add('demo-gtk-logo', icon_set)

    except gobject.GError, error:
        print 'failed to load GTK logo for toolbar'

class ToteMainWindow(gtk.Window):
    def __init__(self, parent=None):
        register_stock_icons()

        # Create the toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(500, 400)

        merge = gtk.UIManager()
        self.set_data("ui-manager", merge)
        merge.insert_action_group(self.__create_action_group(), 0)
        self.add_accel_group(merge.get_accel_group())

        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "building menus failed: %s" % msg
        mainToolBar = merge.get_widget("/MenuBar")
        mainToolBar.show()

        table = gtk.Table(1, 4, False)
        self.add(table)

        table.attach(mainToolBar,
            # X direction #          # Y direction
            0, 1,                      0, 1,
            gtk.EXPAND | gtk.FILL,     0,
            0,                         0);

        mainToolBar = merge.get_widget("/ToolBar")
        mainToolBar.set_tooltips(True)
        mainToolBar.show()
        table.attach(mainToolBar,
            # X direction #       # Y direction
            0, 1,                   1, 2,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)

        contents = gtk.TextView()
        contents.grab_focus()

        #Setting up the Main window:        
        self.mainContentFrame = gtk.Frame()
        table.attach(self.mainContentFrame,
            # X direction           Y direction
            0, 1,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            0,                      0)
            
        vpaned = gtk.VPaned()
        vpaned.set_border_width(5)

        hpaned = gtk.HPaned()
        hpaned.set_border_width(5)
        
        self.quickListFrame = gtk.Frame()
        
        self.quickListFrame.set_label("Add an Item")
        self.quickListTable = gtk.Table(2, 1, False)
        self.quickListFrame.add(self.quickListTable)
        self.quickListEntry = gtk.Entry()
        self.quickListEntry.set_max_length(255)
        self.quickListEntry.set_text("Add new...")
        self.quickListEntry.select_region(0, 10)

        self.quickListCombo = gtk.combo_box_new_text()
        self.quickListCombo.append_text("Task")
        self.quickListCombo.append_text("Event")
        self.quickListCombo.set_active(0)
        
        self.quickListEntry.connect("activate", self.addItem, self.quickListCombo)
        #self.quickListOption.add()
        self.quickListButton = gtk.Button(stock=gtk.STOCK_ADD)
        self.quickListButton.connect("clicked", self.addItem, self.quickListEntry)
    
        self.quickListTable.attach(self.quickListEntry, 0, 1, 0, 1, gtk.EXPAND | gtk.FILL,  gtk.SHRINK, 0, 0)
        self.quickListTable.attach(self.quickListCombo, 1, 2, 0, 1, gtk.SHRINK, gtk.SHRINK, 0, 0)
        self.quickListTable.attach(self.quickListButton, 2, 3, 0, 1, gtk.SHRINK, gtk.SHRINK, 0, 0)
        

        self.mainContentFrame.add(vpaned)
        vpaned.add1(hpaned)
        vpaned.add2(self.quickListFrame)
        
        taskFrame = gtk.Frame()
        calendarFrame = gtk.Frame()
        
        
        hpaned.add1(calendarFrame)
        hpaned.add2(taskFrame)
        
        theNotebook = gtk.Notebook()
        
        self.mainCal = gtk.Calendar()
        calendarFrame.add(self.mainCal)
        self.mainCal.connect("month_changed", self.updateCalendarEvents)
        self.mainCal.connect("prev_year", self.updateCalendarEvents)
        self.mainCal.connect("next_year", self.updateCalendarEvents)
        self.mainCal.connect("day_selected", self.calendar_day_selected)
        self.mainCal.connect("day_selected_double_click", self.calendar_day_selected_double_click)
        
        
        sw_tasks = gtk.ScrolledWindow()
        sw_tasks.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw_tasks.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        notebook_label_tasks = gtk.Label()
        notebook_label_tasks.set_label("Tasks")
        theNotebook.prepend_page(sw_tasks, notebook_label_tasks)
        taskFrame.add(theNotebook)
        
        calTable = gtk.Table(1, 5, False)
        notebook_label_events = gtk.Label()
        notebook_label_events.set_label("Events")
        theNotebook.prepend_page(calTable, notebook_label_events)
        
        sw_both = gtk.ScrolledWindow()
        sw_both.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw_both.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        notebook_label_both = gtk.Label()
        notebook_label_both.set_label("Both")
        theNotebook.append_page(sw_both, notebook_label_both)
        
        #sw_both declarations:
        model_both = self.__create_model_both(nuclasses.tasks, nuclasses.events)
        self.treeview_both = gtk.TreeView(model_both)
        self.treeview_both.set_rules_hint(True)
#        self.treeview_both.set_search_column()
        sw_both.add(self.treeview_both)
        self.__add_columns_both(self.treeview_both)
		
        # create tree model
        model_tasks = self.__create_model_tasks(nuclasses.tasks)

        # create tree view
        self.treeview = gtk.TreeView(model_tasks)
        self.treeview.set_rules_hint(True)
        self.treeview.set_search_column(COLUMN_TASKS_NAME)
        
        sw_tasks.add(self.treeview)

        # add columns to the tree view
        self.__add_columns_tasks(self.treeview)
        
        # Create statusbar
        self.statusbar = gtk.Statusbar()
        table.attach(self.statusbar,
            # X direction           Y direction
            0, 1,                   3, 4,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)


        tselection = self.treeview.get_selection()
        tselection.set_mode(gtk.SELECTION_SINGLE)
        tselection.connect("changed", self.update_statusbar)
        mark_set_callback = (lambda tselection: self.update_statusbar(tselection))
        tselection.connect("changed" , mark_set_callback)
        
        # Show text widget info in the statusbar
        #buffer = contents.get_buffer()
        #buffer.connect("changed", self.update_statusbar)
        #mark_set_callback = (lambda buffer, new_location, mark:
        #    self.update_statusbar(buffer))

        # cursor moved
        #buffer.connect("mark_set", mark_set_callback)#

        self.connect("window_state_event", self.update_resize_grip)
        self.update_statusbar(tselection)

        self.show_all()

    
    def __create_model_both(self, taskList, eventList):
        lstore_both = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)
            #gobject.TYPE_STRING)
            
        for item in taskList:
            iteration = lstore_both.append()
            lstore_both.set(iteration,
                COLUMN_BOTH_COMPLETED, False,
                COLUMN_BOTH_NAME, item.name,
                COLUMN_BOTH_TYPE, "Task",
                COLUMN_BOTH_DATE, item.date,
                COLUMN_BOTH_DESCRIPTION, item.description)
                #COLUMN_BOTH_RELATED, "Nothing")
                
        for item in eventList:
            iteration = lstore_both.append()
            lstore_both.set(iteration,
                COLUMN_BOTH_COMPLETED, False,
                COLUMN_BOTH_NAME, item.name,
                COLUMN_BOTH_TYPE, "Event",
                COLUMN_BOTH_DATE, item.date,
                COLUMN_BOTH_DESCRIPTION, item.description)
                #COLUMN_BOTH_RELATED, "Nothing")
                
        return lstore_both
     
    def addItem(self, widget, entry):
        #text = entry.get_text()
        entryText = self.quickListEntry.get_text()
        comboText = self.quickListCombo.get_active()
        print entryText, comboText
        #print widget, entry, "Text is: ", entry.get_text()
        if comboText == OPTION_ADD_TASK:
            nuclasses.task(entryText)
        elif comboText == OPTION_ADD_EVENT:
            nuclasses.event(entryText)
        else:
            print "A weird error occured... Neither a task nor an event was selected"
        self.treeview_both.set_model(self.__create_model_both(nuclasses.tasks, nuclasses.events))
        self.treeview.set_model(self.__create_model_tasks(nuclasses.tasks))

    def __create_model_tasks(self, taskList):
        lstore_tasks = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
#            gobject.TYPE_UINT,
			gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)

        for item in taskList:
            iter = lstore_tasks.append()
            lstore_tasks.set(iter,
                COLUMN_TASKS_COMPLETED, False,
                COLUMN_TASKS_NAME, item.name,
                COLUMN_TASKS_DUE, nuclasses.shortTime(item.dueTime),
                COLUMN_TASKS_DESCRIPTION, item.description)
        return lstore_tasks

    def fixed_toggled(self, cell, path, model_tasks):
        # get toggled iter
        iter = model_tasks.get_iter((int(path),))
        fixed = model_tasks.get_value(iter, COLUMN_TASKS_COMPLETED)

        # do something with the value
        fixed = not fixed

        # set new value
        model_tasks.set(iter, COLUMN_TASKS_COMPLETED, fixed)

    def __add_columns_both(self, treeview_both):
        model_both = treeview_both.get_model()
        renderer_both = gtk.CellRendererToggle()
        renderer_both.connect('toggled', self.fixed_toggled, model_both)
        
        column = gtk.TreeViewColumn('Done', renderer_both, active=COLUMN_BOTH_COMPLETED)

        # set this column to a fixed sizing(of 50 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)

        treeview_both.append_column(column)

        # column for Name
        column = gtk.TreeViewColumn('Name', gtk.CellRendererText(),
                                    text=COLUMN_BOTH_NAME)
        column.set_sort_column_id(COLUMN_BOTH_NAME)
        treeview_both.append_column(column)

        #Type
        column = gtk.TreeViewColumn('Type', gtk.CellRendererText(),
                                    text=COLUMN_BOTH_TYPE)
        column.set_sort_column_id(COLUMN_BOTH_TYPE)
        treeview_both.append_column(column)

        
        # column for date
        column = gtk.TreeViewColumn('Date', gtk.CellRendererText(),
                                    text=COLUMN_BOTH_DATE)
        column.set_sort_column_id(COLUMN_BOTH_DATE)
        treeview_both.append_column(column)

        # column for description
        column = gtk.TreeViewColumn('Description', gtk.CellRendererText(),
                                     text=COLUMN_BOTH_DESCRIPTION)
        column.set_sort_column_id(COLUMN_BOTH_NAME)
        treeview_both.append_column(column)
        
        #Related
        #column = gtk.TreeViewColumn('Related', gtk.CellRendererText(),
        #                             text=COLUMN_BOTH_RELATED)
        #treeview_both.append_column(column)
        
    
    def __add_columns_tasks(self, treeview):
        model_tasks = treeview.get_model()

        # column for fixed toggles
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.fixed_toggled, model_tasks)

        column = gtk.TreeViewColumn('Done', renderer, active=COLUMN_TASKS_COMPLETED)

        # set this column to a fixed sizing(of 50 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)

        treeview.append_column(column)

        # column for bug numbers
        column = gtk.TreeViewColumn('Name', gtk.CellRendererText(),
                                    text=COLUMN_TASKS_NAME)
        column.set_sort_column_id(COLUMN_TASKS_NAME)
        treeview.append_column(column)

        # columns for severities
        column = gtk.TreeViewColumn('Due', gtk.CellRendererText(),
                                    text=COLUMN_TASKS_DUE)
        column.set_sort_column_id(COLUMN_TASKS_DUE)
        treeview.append_column(column)

        # column for description
        column = gtk.TreeViewColumn('Description', gtk.CellRendererText(),
                                     text=COLUMN_TASKS_DESCRIPTION)
        column.set_sort_column_id(COLUMN_TASKS_NAME)
        treeview.append_column(column)
    def __create_action_group(self):
        # GtkActionEntry
        entries = (
          ( "FileMenu", None, "_File" ),               # name, stock id, label
          ( "PreferencesMenu", None, "_Preferences" ), # name, stock id, label
          ( "NewMenu", None, "_New" ),                   # name, stock id, label
          ( "ColorMenu", None, "_Color"  ),            # name, stock id, label
          ( "ShapeMenu", None, "_Shape" ),             # name, stock id, label
          ( "HelpMenu", None, "_Help" ),               # name, stock id, label
         # ( "New", gtk.STOCK_NEW,                      # name, stock id
         #   "_New", "<control>N",                      # label, accelerator
         #   "Create a new file",                       # tooltip
         #   self.activate_action ),
          ( "Task", gtk.STOCK_DND,
            "_Task", "<control><shift>T",
            "Create a new Task",
            self.activate_action ),
          ( "Event", gtk.STOCK_ADD,
            "_Event", "<control><shift>E",
            "Create a new Event",
            self.activate_action ),
          ( "Project", gtk.STOCK_DND_MULTIPLE,
            "_Project", "<control><shift>P",
            "Create a new Project",
            self.activate_action ),
          ( "Block", gtk.STOCK_DND,
              "_Block", "<control><shift>B",
              "Create a new Block",
              self.activate_action ),
          ( "Open", gtk.STOCK_OPEN,                    # name, stock id
            "_Open","<control>O",                      # label, accelerator
            "Open a file",                             # tooltip
            self.activate_action ),
          ( "Save", gtk.STOCK_SAVE,                    # name, stock id
            "_Save","<control>S",                      # label, accelerator
            "Save current file",                       # tooltip
            self.activate_action ),
          ( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
            "Save _As...", None,                       # label, accelerator
            "Save to a file",                          # tooltip
            self.activate_action ),
          ( "Quit", gtk.STOCK_QUIT,                    # name, stock id
            "_Quit", "<control>Q",                     # label, accelerator
            "Quit",                                    # tooltip
            self.activate_action ),
          ( "About", None,                             # name, stock id
            "_About", "<control>A",                    # label, accelerator
            "About",                                   # tooltip
            self.activate_about ),
          ( "Logo", "demo-gtk-logo",                   # name, stock id
             None, None,                              # label, accelerator
            "GTK+",                                    # tooltip
            self.activate_action ),
        );
        # Gtk... selections?
       # new_entries = (
       #   
       #   )
        # GtkToggleActionEntry
        toggle_entries = (
          ( "Bold", gtk.STOCK_BOLD,                    # name, stock id
             "_Bold", "<control>B",                    # label, accelerator
            "Bold",                                    # tooltip
            self.activate_action,
            True ),                                    # is_active
        )

        # GtkRadioActionEntry
        color_entries = (
          ( "Red", None,                               # name, stock id
            "_Red", "<control><shift>R",               # label, accelerator
            "Blood", COLOR_RED ),                      # tooltip, value
          ( "Green", None,                             # name, stock id
            "_Green", "<control><shift>G",             # label, accelerator
            "Grass", COLOR_GREEN ),                    # tooltip, value
          ( "Blue", None,                              # name, stock id
            "_Blue", "<control><shift>B",              # label, accelerator
            "Sky", COLOR_BLUE ),                       # tooltip, value
        )

        # GtkRadioActionEntry
        shape_entries = (
          ( "Square", None,                            # name, stock id
            "_Square", "<control><shift>S",            # label, accelerator
            "Square",  SHAPE_SQUARE ),                 # tooltip, value
          ( "Rectangle", None,                         # name, stock id
            "_Rectangle", "<control><shift>R",         # label, accelerator
            "Rectangle", SHAPE_RECTANGLE ),            # tooltip, value
          ( "Oval", None,                              # name, stock id
            "_Oval", "<control><shift>O",              # label, accelerator
            "Egg", SHAPE_OVAL ),                       # tooltip, value
        )

        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("AppWindowActions")
        action_group.add_actions(entries)
        action_group.add_toggle_actions(toggle_entries)
        action_group.add_radio_actions(color_entries, COLOR_RED, self.activate_radio_action)
        action_group.add_radio_actions(shape_entries, SHAPE_OVAL, self.activate_radio_action)

        return action_group

    def activate_about(self, action):
        dialog = gtk.AboutDialog()
        dialog.set_name("Tote Life Manager")
        dialog.set_copyright("\302\251 Copyright 2007 Andrew Stromme")
        dialog.set_website("http://tote.chatonka.com/")
        ## Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_radio_action(self, action, current):
        active = current.get_active()
        value = current.get_current_value()

        if active:
            dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                "You activated radio action: \"%s\" of type \"%s\".\nCurrent value: %d" %
                (current.get_name(), type(current), value))

            # Close dialog on user response
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()

    def update_statusbar(self, buffer):
        # clear any previous message, underflow is allowed
        self.statusbar.pop(0)
        # count = buffer.get_char_count()
        (model, iter) = buffer.get_selected()
        
        #iter = buffer.get_iter_at_mark(buffer.get_insert())
        # row = iter.get_line()
        # col = iter.get_line_offset()
        print iter
        if iter != None:
            nameData = model.get(iter, COLUMN_TASKS_NAME)[0]
            dateData = model.get(iter, COLUMN_TASKS_DUE)[0]
            print nameData, dateData
            #hoursFromNow = nuclasses.timeBetweenTimes(time1, time2)
            hoursFromNow = "<Sorry - Incomplete>"
            self.statusbar.push(0,
        '%s is due %s hours. This is %s hours from now' % (nameData, dateData, hoursFromNow))
        else:
            self.statusbar.push(0,
        'No Task Selected')

    def update_resize_grip(self, widget, event):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))
            
    def updateCalendarEvents(self, widget): #strings
        self.calendarDateToTuple(widget)
        pass
        
    def calendar_day_selected(self, widget):
        theDate = self.calendarDateToString(widget)
        items = nuclasses.findItemsForDate(theDate)
        taskList = []
        eventList = []
        for item in items:
            print item.__class__.__name__
            if item.__class__.__name__ == "task":
                taskList.append(item)
            elif item.__class__.__name__ == "event":
                eventList.append(item)
            else:
                pass
        self.treeview.set_model(self.__create_model_tasks(taskList))
        self.treeview_both.set_model(self.__create_model_both(taskList, eventList))
        print taskList, eventList
    
    def calendar_day_selected_double_click(self, widget):
        pass
    
    def calendarDateToTuple(self, calendar):
        year, month, day = calendar.get_date()
        theTime = time.localtime(time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1)))
        return theTime
    
    def calendarDateToString(self, calendar):
        theTime = self.calendarDateToTuple(calendar)
        print theTime
        theDate = nuclasses.dateFromTime(theTime)
        return theDate




def main():
    ToteMainWindow()
    gtk.main()

if __name__ == '__main__':
    main()
