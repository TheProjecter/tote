#~/usr/bin/env python

import pygtk
#pygtk.require('2.0') no require?
import gtk
import gui_pygtk.layoutFunctions


def sys_icon_pixbuf(icon_name, size=36):
    return gtk.icon_theme_get_default().load_icon(icon_name, size, 0)



class Base_Window:
        def default(self, widget, data=None):
            print "Widget %s" % widget
            print "Not Finished Yet!"
            
        def __init__(self):
            self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.window.connect("delete_event", self.delete_event)
            self.window.connect("destroy", self.destroy)
            self.window.set_border_width(10)
            self.window.set_title("Tote")
            
            self.table_main = gtk.Table(2, 2, True)
            self.window.add(self.table_main)
            self.table_buttons = gtk.Table(4, 1, True)
            self.table_buttons.set_col_spacings(3)
            self.table_main.attach(self.table_buttons, 0, 1, 0, 1)
            
            self.treestore = gtk.TreeStore(str)
            
            stuff = gui_pygtk.layoutFunctions.organize_for_tree(self.treestore)
            stuff = (stuff[0], ["Hey", "YO"])
            print stuff
            for each in stuff[0]:
                classiter = self.treestore.append(None, [each])
                for this in stuff[1]:
                    self.treestore.append(classiter, [this])
        
                
            self.treeview = gtk.TreeView(self.treestore)
            self.tvcol = gtk.TreeViewColumn('Column 0')
            self.treeview.append_column(self.tvcol)
            self.treecell = gtk.CellRendererText()
            self.tvcol.pack_start(self.treecell, True)
            self.tvcol.add_attribute(self.treecell, 'text', 0)
            self.treeview.set_search_column(0)

            self.tvcol.set_sort_column_id(0)
            self.treeview.set_reorderable(True)
            self.table_main.attach(self.treeview, 0, 1, 1, 2)
            self.table_main.show_all()
            self.treeview.show()
            
#            self.separator1 = gtk.VSeparator()
#            self.table_buttons.attach(self.separator1, 2, 3, 0, 1)
#            self.separator1.show()
            
            
            self.button_add = gtk.Button(stock=gtk.STOCK_ADD)
            self.button_remove = gtk.Button(stock=gtk.STOCK_REMOVE)
            self.button_about = gtk.Button(stock=gtk.STOCK_ABOUT)
            
            self.button_add.connect("clicked", self.default, None)
            self.button_remove.connect("clicked", self.default, None)
            self.button_about.connect("clicked", self.about_window, None)

            self.table_buttons.attach(self.button_add, 0, 1, 0, 1)
            self.table_buttons.attach(self.button_remove, 1, 2, 0, 1)
            self.table_buttons.attach(self.button_about, 3, 4, 0, 1)

            self.tooltips_main = gtk.Tooltips()
            self.tooltips_main.set_tip(self.button_add, "Creates a new Task", tip_private=None)
            self.tooltips_main.set_tip(self.button_remove, "Removes selected task", tip_private=None)

            self.table_main.show()
            self.table_buttons.show()
            self.button_add.show()
            self.button_remove.show()
            self.button_about.show()
            self.window.show()
            
            
        def destroy(self, widget, data=None):
            gtk.main_quit()
        
        def delete_event(self, widget, event, data=None):
            print 'delete even occured'    
            
        def about_window(self, widget, event, data=None):
            sw = gtk.ScrolledWindow()
            sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            aboutbox = gtk.TextView(buffer=None)
            aboutbox.set_wrap_mode(gtk.WRAP_WORD)
            aboutbox.set_editable(0)
            sw.add(aboutbox)
            sw.show()
            dialog = gtk.Dialog(title="About Tote", parent=None, flags=0, buttons=None)
            dialog.set_border_width(5)
            aboutbox.get_buffer().set_text("Tote - Keeping track of Life\n\n By Andrew Stromme\n blah blah blah\n")
            button = gtk.Button(label="Close")
            button.connect("clicked", lambda a : dialog.destroy())
            dialog.action_area.pack_start(button, True, True, 0)
            button.show()

            label = gtk.Label("Dialogs are groovy")
            dialog.vbox.pack_start(sw, True, True, 5)
            aboutbox.show()
            #label.show()
            dialog.show()
            dialog.set_size_request(200, 200)
              
        def main(self):
            gtk.main()
            
        
        
        
#Can be removed
print __name__
if __name__ == "__main__":
    base = Base_Window()
    base.main()
