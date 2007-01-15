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

        self.pbar = self.wTree.get_widget("pbar")

        # if you forget to show the main window it's gonna be a sad gui
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).

        gtk.main()

    def startpytof(self, widget):
        po = pytofOptions()
        po.check()

        progress = ProgressMsg(-1, self.pbar)
        pytof = Pytof(po, progress)
        pytof.main()


if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
