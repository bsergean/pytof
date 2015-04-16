#!/usr/bin/env python
# example colorsel.py

import pygtk
pygtk.require('2.0')
import gtk

class FloatColor:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def gtkColor(self):
        return gtk.gdk.Color(int(self.r * 65535.0),
                             int(self.g * 65535.0),
                             int(self.b * 65535.0))

class ColorLabel:
    def __init__(self, name, color):
        label = gtk.Label(name)
        label.modify_fg(gtk.STATE_NORMAL, color.gtkColor())
        label.show()
        self.widget = label

class ColorList:
    def __init__(self):
        # Create toplevel window, set title and policies
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.modify_bg(gtk.STATE_NORMAL, FloatColor(1,1,1).gtkColor())
        self.window.set_title("Color List")

    def createLabels(self):
        colors = '''
0.000000,0.000000,0.000000
0.172549,0.301961,0.431373
0.000000,0.000000,1.000000
0.000000,1.000000,0.000000
1.000000,0.000000,0.000000
0.815686,0.815686,0.815686
0.815686,0.815686,0.815686
0.780392,0.278431,0.654902
0.278431,0.611765,0.137255
0.400000,0.400000,0.800000
0.815686,0.815686,0.815686
0.000000,0.000000,0.000000'''
        
        text = colors
        cols = 3
        rows = colors.count('\n') / cols
        colorLabArray = []
        
        for line in text.splitlines():
            if not line: continue
            fc = FloatColor(*map(float, line.split(',')))
            lab = line
            colorLab = ColorLabel(lab, fc)
            colorLabArray.append(colorLab)

        

        col = 0
        self.vb = gtk.VBox(True, 10)
        hb = gtk.HBox(True, 10)
        self.vb.pack_start(hb)
        
        for cl in colorLabArray:
            hb.pack_start(cl.widget)
            
            col += 1
        
            if col % (cols) == 0:
                col = 0
                hb.show()
                hb = gtk.HBox(True, 10)
                self.vb.pack_start(hb)

    def show(self):
        self.createLabels()
        self.window.add(self.vb)
        self.vb.show()
        self.window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    try:
        cl = ColorList()
        cl.show()
        main()
    except KeyboardInterrupt:
        pass
