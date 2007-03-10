How to distribute python programs as .exe using py2exe
------------------------------------------------------

1. Have Python and corresponding version of py2exe installed

2. Make a setup script (see setup-ftpd.py for the script to build from ftpd.py)

3. run:
   your-setup-script.py py2exe --help
   to see the command line options.

4. run (for example):
   your-setup-script.py py2exe --windows
   to build an executable that runs as a Windows application.
   You can specify an icon using "--icon filename.ico"

5. In the dist directory is a directory containing the .exe and necessary DLLs. Distribute that.


 