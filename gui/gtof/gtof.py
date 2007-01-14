#!/usr/bin/env python

# example helloworld.py

import sys
sys.path.insert(1, '../../pytof')

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

from options import pytofOptions
from pytofmain import main


class HelloWorld:

    def __init__(self):
        self.gladefile = "gtof.glade"
        self.wTree = gtk.glade.XML(self.gladefile) 
        
        #Get the Main Window, and connect the "destroy" event
        self.window = self.wTree.get_widget("gtof")
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)

        self.button = self.wTree.get_widget("button1")
        if (self.button):
            self.button.connect("clicked", self.startpytof)

        # if you forget to show the main window it's gonna be a sad gui
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).

        gtk.main()

    def startpytof(self, widget):
        options = pytofOptions()
        main(options.albumName, options.libraryPath,
             options.xmlFileName, options.outputDir,
             options.info, options.fs, options.tar,
             options.Zip, options.ftp, options.strip_originals,
             options.fromDir)


if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
