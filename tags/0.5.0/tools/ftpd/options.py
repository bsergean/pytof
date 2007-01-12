# options.py
# Copyright (C) 2002 Peter Harris and Kyndal International
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

"""options(syntaxdict,argv) converts a list of strings to a dict of
 options, using the syntaxdict to determine what kinds of options to expect.

 The keys of the syntax dict are the option names, including leading '-' or '--'
 The values of the syntax dict are the default values and indicate the kind
 of option:

 0,1    : accept --name to set 1 , --no-name to set 0
 string : accept --name and overwrite with next string from list
 list   : accept --name and concat next_string.split(",") to list
 tuple  : like list, but overwrite first time, treat as list thereafter

 For options beginning with one '-', the value is the long name of the option,
 which should also be in the syntax dict.

 The tail of the command line and any unrecognised strings are always returned
 in the value of option '--', and if '--' is found on the command line,
 everything that follows is the tail, whether it looks like an option or not.
"""
from types import NoneType,IntType,StringType,TupleType,ListType
def options(syntaxdict,argv):
    opts={}
    opts['--']=[] # to hold the command tail
    for k,v in syntaxdict.items():
        if k[:2] == '--':
            opts[k]=v
    args=argv[:]  # a copy I can modify safely
    while args:
        arg=args.pop(0)
        if arg[0]=='-' and len(arg) > 1: # an option
            if arg[1] != '-': # single hyphen (short) option
                arg=syntaxdict.get(arg,arg) # look up long one if there
            if arg == '--':  # end of options
                opts['--'].extend(args) # command tail
                break  # all done
            flagvalue=1 # in case we are dealing with a boolean
            if arg[:5] == '--no-':
                arg='--' + arg[5:]
                flagvalue=0
            current=opts.get(arg,None)
            t=type(current)
            if t == NoneType:
                opts['--'].append(arg)  # no idea what this option is
            elif t == IntType:
                opts[arg]=flagvalue
            else:
                try:
                    next=args.pop(0)
                    if t == StringType:
                        opts[arg]=next
                    elif t == TupleType:
                        opts[arg]=next.split(",")
                    elif t == ListType:
                        opts[arg].extend(next.split(","))
                    else:
                        pass # dodgy syntax entry
                except:
                    pass # no next argument
        else: # not an option
            opts['--'].append(arg)
    return opts

if __name__ == '__main__':
    import sys
    print """
    Test by passing options:
      --flag, --no-flag : boolean
      --list1 , -L :  list of strings, comma separated
      --string, -s :  single string
      --list2, -D  : list of strings (replaces default 'hello')
      """
    print options({'--flag':0,'--list1':[],'-L':'--list1','--string':'',
                   '-s':'--string','--list2':('hello',),'-D':'--list2'},
                  sys.argv[1:])
