#!/usr/bin/env python
"""
Main User interface for pytof, based on pygtk.
Currently it is very basic, just a file selection dialog
and a go button.
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

import sys
from os.path import join, expanduser
from os import sep, pardir
sys.path.insert(1, join(pardir, 'pytof'))

try:
    import pygtk
    pygtk.require('2.0')
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    from pytof.options import _err_exit
    _err_exit('You need to install pygtk to use gtof. Sorry...')

from pytof.options import PytofOptions
from pytof.pytofmain import Pytof
from pytof.utils import ProgressMsg

class ProgressMsg(object):

    ''' General purpose progress bar '''
    
    def __init__(self, target, pbar):
        self.pbar = pbar
        self.counter = 0.0
        self.target = float(target)

    def Increment(self):
        '''
        FIXME: I guess there is a better way to do, like connecting the
        progress bar to the main application, or something like that, than
        calling gtk.main_iteration() to update the progress bar
        '''
        self.counter += 1
        self.pbar.set_fraction(self.counter / self.target)       
        if self.counter == self.target:
            self.pbar.set_fraction(1)

        gtk.main_iteration()

class FileSelection:
    def file_ok_sel(self, w):
        '''
        Get the selected filename and print it to the console
        '''
        print "%s" % self.filew.get_filename()
        self.parent.dir = self.filew.get_filename()
        self.filew.destroy()

    def __init__(self, parent, dirName):

        self.parent = parent
        
        # Create a new file selection widget
        self.filew = gtk.FileSelection("File selection")

        # Connect the ok_button to file_ok_sel method
        self.filew.ok_button.connect("clicked", self.file_ok_sel)
    
        # Connect the cancel_button to destroy the widget
        self.filew.cancel_button.connect("clicked",
                                         lambda w: self.filew.destroy())
    
        # Lets set the filename, as if this were a save dialog,
        # and we are giving a default filename
        self.filew.set_filename(dirName)
    
        self.filew.show()

class HelloWorld:

    def __init__(self):
    	gladeDir = join(sys.prefix, 'share', 'pytof', 'glade')
        self.gladefile = join(gladeDir, 'gtof.glade')
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

	homeDir = expanduser('~')
	self.dirName = homeDir
	print self.dirName
        # if you forget to show the main window it's gonna be a sad gui
        self.window.show()

    def fileSelection(self, widget):        
        fs = FileSelection(self, self.dirName)

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).

        gtk.main()

    def startpytof(self, widget):
        po = pytofOptions()
        if not po.options.fromDir: # not from command line
            if not self.dir:
                sys.exit(1)
            else:
                po.options.fromDir = self.dir

        localEncoding = sys.stdout.encoding
        if localEncoding == 'cp850':
            po.options.fromDir = po.options.fromDir.encode('latin1')
            print po.options.fromDir

        po.check()

        progress = ProgressMsg(-1, self.pbar)
        pytof = Pytof(po, progress)
        pytof.main()

def main():
    hello = HelloWorld()
    hello.main()

if __name__ == "__main__":
    main()
