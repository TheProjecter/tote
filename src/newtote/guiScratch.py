#!/usr/bin/env python

import gobject
import gtk
import nuclasses
import icalHandler
import zohoApiInteraction
import time
import datetime

treeitems_uids = {}
treetasks_uids = {}

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
    COLUMN_TASKS_DESCRIPTION,
    COLUMN_TASKS_UID
) = range(5)

(
    COLUMN_BOTH_COMPLETED,
    COLUMN_BOTH_NAME,
    COLUMN_BOTH_TYPE,
    COLUMN_BOTH_DATE,
    COLUMN_BOTH_DESCRIPTION,
    COLUMN_BOTH_UID,
    COLUMN_BOTH_RELATED
) = range(7)
 
(
    OPTION_ADD_TASK,
    OPTION_ADD_EVENT
) = range(2)

(
    NOTEBOOK_EVENTS,
    NOTEBOOK_TASKS,
    NOTEBOOK_BOTH
) = range(3)

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
      <menuitem action='Remove'/>
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
    <toolitem action='Remove'/>
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
        nuclasses.log_error('failed to load GTK logo for toolbar')

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
            nuclasses.log_error("building menus failed: %s" % msg)
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
        
        self.theNotebook = gtk.Notebook()
        
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
        self.theNotebook.prepend_page(sw_tasks, notebook_label_tasks)
        taskFrame.add(self.theNotebook)
        
        calTable = gtk.Table(1, 5, False)
        notebook_label_events = gtk.Label()
        notebook_label_events.set_label("Events")
        self.theNotebook.prepend_page(calTable, notebook_label_events)
        
        sw_both = gtk.ScrolledWindow()
        sw_both.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw_both.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        notebook_label_both = gtk.Label()
        notebook_label_both.set_label("Both")
        self.theNotebook.append_page(sw_both, notebook_label_both)
        
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

    def __build_column_data_pairs(self, item, itemData):
        column_data_pairs = []
        for number in range(len(itemData)):
            column_data_pairs.append(number)
            column_data_pairs.append(item.get_data[itemData[number]])
        return column_data_pairs
    

    def __create_model(self, columnData, itemList, itemData): #ItemData is a list of things for columns. columnData[0] links up with itemData[0]
        lstore = gtk.ListStore(*columnData)

        for item in itemList:
            iteration = lstore.append()
            treeitems_uids[iteration] = item.uid
            column_data_pairs = self.__build_column_data_pairs(item, itemData)
            lstore.set(iteration, *column_data_pairs)
            
    def __create_model_both(self, taskList, eventList):
        lstore_both = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)
            #gobject.TYPE_STRING)
            
        for item in taskList:
            iteration = lstore_both.append()
            treeitems_uids[iteration] = item.uid
            lstore_both.set(iteration,
                COLUMN_BOTH_COMPLETED, False,
                COLUMN_BOTH_NAME, item.name,
                COLUMN_BOTH_TYPE, "Task",
                COLUMN_BOTH_DATE, item.getdate(),
                COLUMN_BOTH_DESCRIPTION, item.description,
                COLUMN_BOTH_UID, item.uid)
                #COLUMN_BOTH_RELATED, "Nothing")
                
        for item in eventList:
            iteration = lstore_both.append()
            treeitems_uids[iteration] = item.uid
            lstore_both.set(iteration,
                COLUMN_BOTH_COMPLETED, False,
                COLUMN_BOTH_NAME, item.name,
                COLUMN_BOTH_TYPE, "Event",
                COLUMN_BOTH_DATE, item.getdate(),
                COLUMN_BOTH_DESCRIPTION, item.description,
                COLUMN_BOTH_UID, item.uid)
                #COLUMN_BOTH_RELATED, "Nothing")
                
        return lstore_both
     
    def addItem(self, widget, entry):
        #text = entry.get_text()
        entryText = self.quickListEntry.get_text()
        comboText = self.quickListCombo.get_active()
        #print widget, entry, "Text is: ", entry.get_text()
        if comboText == OPTION_ADD_TASK:
            nuclasses.task(entryText)
        elif comboText == OPTION_ADD_EVENT:
            nuclasses.event(entryText)
        else:
            nuclasses.log_error("A weird error occured... Neither a task nor an event was selected")
        self.treeview_both.set_model(self.__create_model_both(nuclasses.tasks, nuclasses.events))
        self.treeview.set_model(self.__create_model_tasks(nuclasses.tasks))

    def __create_model_tasks(self, taskList):
        lstore_tasks = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
#            gobject.TYPE_UINT,
			gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)

        for item in taskList:
            iter = lstore_tasks.append()
            treetasks_uids[iter] = item.uid
            lstore_tasks.set(iter,
                COLUMN_TASKS_COMPLETED, False,
                COLUMN_TASKS_NAME, item.name,
                COLUMN_TASKS_DUE, nuclasses.shortTime(item.dueTime),
                COLUMN_TASKS_DESCRIPTION, item.description,
                COLUMN_TASKS_UID, item.uid)
        return lstore_tasks

    def fixed_toggled(self, cell, path, model_tasks):
        # get toggled iter
        iter = model_tasks.get_iter((int(path),))
        fixed = model_tasks.get_value(iter, COLUMN_TASKS_COMPLETED)

        # do something with the value
        fixed = not fixed

        # set new value
        model_tasks.set(iter, COLUMN_TASKS_COMPLETED, fixed)
        
    def update_treeview_text(self, cell, path, new_text, model, column):
        """
        Called when a text cell is edited. It puts the new text
        in the model so that it is displayed properly.
        """
        model[path][column] = new_text
        nuclasses.taskFromUid(model[path][COLUMN_TASKS_UID]).description = new_text

    def __add_columns_both(self, treeview_both):
        """
        Updates the items in the TreeView for the 'both' tab
        """
        model_both = treeview_both.get_model()
        renderer_both = gtk.CellRendererToggle()
        renderer_both.connect('toggled', self.fixed_toggled, model_both)
        
        renderer_text = gtk.CellRendererText()
        renderer_text.set_property( 'editable', True )
        renderer_text.connect( 'edited', self.update_treeview_text, model_both, COLUMN_BOTH_DESCRIPTION)
        
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
        
        renderer_text = gtk.CellRendererText()
        renderer_text.set_property( 'editable', True )
        renderer_text.connect( 'edited', self.update_treeview_text, model_tasks, COLUMN_TASKS_DESCRIPTION)

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
        column = gtk.TreeViewColumn('Description', renderer_text,
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
            self.activate_open ),
          ( "Remove", gtk.STOCK_DELETE,
            "_Remove","<Delete>",
            "Remove selected item",
            self.activate_remove ),
          ( "Save", gtk.STOCK_SAVE,                    # name, stock id
            "_Save","<control>S",                      # label, accelerator
            "Save current file",                       # tooltip
            self.activate_save ),
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
        a = icalHandler.tasksToVObject(nuclasses.tasks)
        (b, c) = icalHandler.itemsFromVObject(a.serialize())
        icalHandler.addTasksFromCalDict(b)
        dialog.show()

    def activate_remove(self, action):
        page = self.theNotebook.get_current_page()
        if page == NOTEBOOK_BOTH:
            (store, iter) = self.treeview_both.get_selection().get_selected()
            uid = store.get(iter, COLUMN_BOTH_UID)
            column_name = COLUMN_BOTH_NAME
            type = store.get(iter, COLUMN_BOTH_TYPE)[0]
            if type == "Task": #Yes, it's only capitalized in this instance
                type = "task"
                item = nuclasses.taskFromUid(uid[0])
            elif type == "Event":
                type = "event"
                item = nuclasses.eventFromUid(uid[0])
            else:
                nuclasses.log_error("Error: Could not determine type. Item '%s' did not match either Task or Event." % type)
        elif page == NOTEBOOK_TASKS:
            (store, iter) = self.treeview.get_selection().get_selected()
            uid = store.get(iter, COLUMN_TASKS_UID)
            column_name = COLUMN_TASKS_NAME
            item = nuclasses.taskFromUid(uid[0])
        elif page == NOTEBOOK_EVENTS:
            pass
        else:
            nuclasses.log_error("No page selected? Error with determining the active notebook page")
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, 
            'Do you really want to remove the %s: "%s"' % (item.__name__, store.get(iter, column_name)[0]))
        def do_response(d, r):
            d.destroy()
            if r == -9:
                pass
            elif r == -8:
                try:
                    nuclasses.tasks.remove(item)
                except:
                    nuclasses.events.remove(item)
                self.treeview_both.set_model(self.__create_model_both(nuclasses.tasks, nuclasses.events))
                self.treeview.set_model(self.__create_model_tasks(nuclasses.tasks))
        dialog.connect("response", do_response)
        dialog.show()
        
        

    def activate_open(self, action):
        tempdict = icalHandler.importiCalFromFile("/home/astromme/icaltest.ics")
        icalHandler.addTasksFromCalDict(tempdict)
        self.treeview_both.set_model(self.__create_model_both(nuclasses.tasks, nuclasses.events))
        self.treeview.set_model(self.__create_model_tasks(nuclasses.tasks))
        
    def activate_save(self, action):
        icalObject = icalHandler.tasksToVObject(nuclasses.tasks)
        icalHandler.exportiCalToFile(icalObject, "/home/astromme/icaltest.ics",1)
        

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
        
        if iter != None:
            nameData = model.get(iter, COLUMN_TASKS_NAME)[0]
            dateData = model.get(iter, COLUMN_TASKS_DUE)[0]
            timeNow = datetime.datetime.now()
            timeOfTask = nuclasses.taskFromUid(model.get(iter, COLUMN_TASKS_UID)[0]).dueTime
            if timeOfTask == None:
                messageString = "There is no due date set for '%s'" % (nameData)
            else:
                delta = timeOfTask - timeNow
                deltaHours = nuclasses.secondsToHours(delta.seconds, 1)
                if delta.days < 0: #Task due in the past
                    if delta.days <= -2: #If it was due at least one day ago, we put days and hours
                        deltaDays = -(delta.days) - 1 #Negative day format is given as -Xdays, +Yseconds
                        deltaHours = nuclasses.secondsToHours(24*3600 - delta.seconds, 1) #function(seconds, roundDown?)
                        messageString = "%s was due % days and % hours ago. Yikes!" % (nameData, deltaDays, deltaHours)
                    elif delta.days > -2: #Otherwise, we only put hours
                        messageString = "%s was due % hours ago. Yikes!" % (nameData, deltaHours)
                        if deltaHours < 4:
                            if deltaHours < 1:
                                (deltaHours, deltaMinutes) = nuclasses.secondsToHoursMinutes(24*3600 - delta.seconds, 1) # function(seconds, round down?)
                                messageString = "%s was due % minutes ago. Yikes!" % (nameData, deltaMinutes)
                            else:
                                (deltaHours, deltaMinutes) = nuclasses.secondsToHoursMinutes(24*3600 - delta.seconds, 1) # function(seconds, round down?)
                                messageString = "%s was due % hours and % minutes ago. Yikes!" % (nameData, deltaHours, deltaMinutes)
                        
                elif delta.days >= 0: #Task due in the future
                    if delta.days >= 1: #If it will be due >1 day, put days + hours
                        deltaDays = delta.days
                        deltaHours = nuclasses.secondsToHours(delta.seconds, 1) #function(seconds, roundDown?)
                        messageString = "%s is due %s hours. This is %s days and %s hours from now" % (nameData, dateData, deltaDays, deltaHours)
                    elif delta.days < 1: #Otherwise, we only put hours
                        if deltaHours < 4:
                            if deltaHours < 1:
                                (deltaHours, deltaMinutes) = nuclasses.secondsToHoursMinutes(delta.seconds, 1) # function(seconds, round down?)
                                messageString = '%s is due in %s minutes!' % (nameData, deltaMinutes)                        
                            else:
                                (deltaHours, deltaMinutes) = nuclasses.secondsToHoursMinutes(delta.seconds, 1) # function(seconds, round down?)
                                messageString = '%s is due %s hours. This is %s hours and %s minutes from now' % (nameData, dateData, deltaHours, deltaMinutes)
                        else:
                            messageString = '%s is due %s hours. This is %s hours from now' % (nameData, dateData, deltaHours)
            self.statusbar.push(0, messageString)        
            hoursFromNow = "<Sorry - Incomplete>"
            #self.statusbar.push(0,
        #'%s is due %s hours. This is %s hours from now' % (nameData, dateData, hoursFromNow))
        else:
            self.statusbar.push(0,
        'No Task Selected')

    def update_resize_grip(self, widget, event):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))
            
    def updateCalendarEvents(self, widget): #strings
        theTime = self.calendarDateToDateTime(widget)
        
        pass
        
    def calendar_day_selected(self, widget):
        theDate = self.calendarDateToString(widget)
        items = nuclasses.findItemsForDate(theDate)
        taskList = []
        eventList = []
        for item in items:
            nuclasses.log_info("Item.__class__.__name__ is: %s" % item.__class__.__name__)
            if item.__class__.__name__ == "task":
                taskList.append(item)
            elif item.__class__.__name__ == "event":
                eventList.append(item)
            else:
                pass
        self.treeview.set_model(self.__create_model_tasks(taskList))
        self.treeview_both.set_model(self.__create_model_both(taskList, eventList))
        nuclasses.log_info("Here is the taskList, eventList: %s %s" % (taskList, eventList))
    
    def calendar_day_selected_double_click(self, widget):
        pass

    def calendarDateToDateTime(self, calendar):
        year, month, day = calendar.get_date()
        nuclasses.log_info("Here is the year, month, day: %s %s %s" % (year, month, day))
        theTime = datetime.datetime(year, month+1, day)
        return theTime
    
    def calendarDateToString(self, calendar):
        theTime = self.calendarDateToDateTime(calendar)
        theDate = nuclasses.dateFromTime(theTime)
        return theDate




def main():
    ToteMainWindow()
    gtk.main()

if __name__ == '__main__':
    main()
