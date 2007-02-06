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
from pytofmain import Pytof
from utils import ProgressMsg

class ProgressMsg(object):
    """ General purpose progress bar """
    def __init__(self, target, pbar):
        self.pbar = pbar
        self.counter = 0.0
        self.target = float(target)

    def Increment(self):
        self.counter += 1
        self.pbar.set_fraction(self.counter / self.target)       
        if self.counter == self.target:
            self.pbar.set_fraction(1)

        # FIXME: I guess there is a better way to do, like connecting the
        # progress bar to the main application, or something like that.
        gtk.main_iteration()

class FileSelection:
    # Get the selected filename and print it to the console
    def file_ok_sel(self, w):
        print "%s" % self.filew.get_filename()
        self.filew.destroy()

    def __init__(self):
        # Create a new file selection widget
        self.filew = gtk.FileSelection("File selection")

        # Connect the ok_button to file_ok_sel method
        self.filew.ok_button.connect("clicked", self.file_ok_sel)
    
        # Connect the cancel_button to destroy the widget
        self.filew.cancel_button.connect("clicked",
                                         lambda w: self.filew.destroy())
    
        # Lets set the filename, as if this were a save dialog,
        # and we are giving a default filename
        self.filew.set_filename('')
    
        self.filew.show()

class HelloWorld:

    def __init__(self):
        self.gladefile = "gtof.glade"
        self.wTree = gtk.glade.XML(self.gladefile) 
        
        #Get the Main Window, and connect the "destroy" event
        self.window = self.wTree.get_widget("gtof")
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)

        self.dirButton = self.wTree.get_widget("dirButton")
        if (self.dirButton):
            self.dirButton.connect("clicked", self.fileSelection)

        self.startButton = self.wTree.get_widget("startButton")
        if (self.startButton):
            self.startButton.connect("clicked", self.startpytof)

        self.pbar = self.wTree.get_widget("pbar")
        self.label = self.wTree.get_widget("pbar") # strange

        # if you forget to show the main window it's gonna be a sad gui
        self.window.show()

        # data init
        self.dir = ''

    def fileSelection(self, widget):
        fs = FileSelection()
        self.dir = fs.filew.get_filename()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).

        gtk.main()

    def startpytof(self, widget):
        po = pytofOptions()
        po.options.fromDir = self.dir
        po.check()

        progress = ProgressMsg(-1, self.pbar)
        pytof = Pytof(po, progress)
        pytof.main()


if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
