import gtk
import pygtk
import conf.configInit
import Base.functions as gf
import os

def picture_label_from_xpm(parent, xpm_filename, label_text, vertical=1):
    if vertical == 1:
        box = gtk.VBox(False, 0)
    else:
        box = gtk.HBox(False, 0)
    box.set_border_width(2)

    image = gtk.Image()
    image.set_from_filename(xpm_filename)
    label = gtk.Label(label_text)

    # Pack the pixmap and label into the box
    box.pack_start(image, False, False, 1)
    box.pack_start(label, False, False, 1)
    

    image.show()
    label.show()
    return box
  
    
def picture_label_from_pixbuf(parent, pixbuf, label_text, vertical=1):
    if vertical == 1:
        box = gtk.VBox(False, 0)
    else:
        box = gtk.HBox(False, 0)
    box.set_border_width(2)

    image = gtk.Image()
    image.set_from_pixbuf(pixbuf)
    label = gtk.Label(label_text)

    # Pack the pixmap and label into the box
    box.pack_start(image, False, False, 3)
    box.pack_start(label, False, False, 3)

    image.show()
    label.show()
    return box

def organize_for_tree(treestore):
    hrClassList = conf.configInit.grab_class_config() #hrClasslist
    openTasks = gf.loadTasks(os.path.expanduser(conf.configInit.grab_file_locations()[0]))
    return (hrClassList, openTasks)
    
        
