#!/usr/bin/env python

# example helloworld.py

import sys
try:
    import pygtk
    pygtk.require('2.0')
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class HelloWorld:

    def __init__(self):
        self.gladefile = "gtof.glade"
        self.wTree = gtk.glade.XML(self.gladefile) 
        
        #Get the Main Window, and connect the "destroy" event
        self.window = self.wTree.get_widget("gtof")
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)
            
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
