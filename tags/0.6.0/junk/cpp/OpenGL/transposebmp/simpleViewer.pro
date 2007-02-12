# The simplest application example: 20 lines of code and yet all the power !

# A Viewer class is derived from QGLViewer and its <code>draw()</code> function is overloaded to
# specify the user defined OpenGL orders that describe the scene.

# This is the first example you should try, as it explains some of the default keyboard shortcuts
# and the mouse behavior of the viewer.

# This example can be cut and pasted to start the development of a new application. 


TEMPLATE = app
TARGET   = simpleViewer
CONFIG  += qt opengl warn_on release thread

HEADERS  = simpleViewer.h
SOURCES  = simpleViewer.cpp main.cpp

##  Windows Qt 2.3 users should uncomment the next 2 lines and remove all the remaining lines.
#DEFINES *= QT_DLL QT_THREAD_SUPPORT
#LIBS *= QGLViewer.lib


# Unix : same INCLUDE_DIR and LIB_DIR parameters than for the make install
# Try to autodetect in ../.. if not found and not defined
unix {
  isEmpty( PREFIX ) {
    PREFIX=/usr/local
  }

  # INCLUDE_DIR
  isEmpty( INCLUDE_DIR ) {
    INCLUDE_DIR = $$PREFIX/include

    !exists( $$INCLUDE_DIR/QGLViewer/qglviewer.h ) {
      exists( ../../QGLViewer/qglviewer.h ) {
        message( Using ../.. as INCLUDE_DIR )
        INCLUDE_DIR = ../..
      }
    }
  }

  !exists( $$INCLUDE_DIR/QGLViewer/qglviewer.h ) {
    message( Unable to find QGLViewer/qglviewer.h in $$INCLUDE_DIR )
    message( Use qmake INCLUDE_DIR~Path/To/QGLViewer/HeaderFiles )
    error( Replace the ~ by the "equals" character in the above line )
  }

  # LIB_NAME
  LIB_NAME = libQGLViewer.so*
  macx {
    LIB_NAME = libQGLViewer.*.$$QMAKE_EXTENSION_SHLIB
  }
  darwin-g++ {
    LIB_NAME = libQGLViewer.*.$$QMAKE_EXTENSION_SHLIB
  }
  hpux {
    LIB_NAME = libQGLViewer.sl*
  }

  # LIB_DIR
  isEmpty( LIB_DIR ) {
    LIB_DIR = $$PREFIX/lib

    !exists( $$LIB_DIR/$$LIB_NAME ) {
      exists( ../../QGLViewer/$$LIB_NAME ) {
        message( Using ../../QGLViewer as LIB_DIR )
        LIB_DIR = ../../QGLViewer
      }
    }
  }

  !exists( $$LIB_DIR/$$LIB_NAME ) {
    message( Unable to find $$LIB_NAME in $$LIB_DIR )
    message( You should run qmake LIB_DIR~Path/To/QGLViewer/Lib )
    error( Replace the ~ by the "equals" character in the above line )
  }

  # Path was correctly detected
  INCLUDEPATH *= $$INCLUDE_DIR
  DEPENDPATH  *= $$INCLUDE_DIR
  LIBS        *= -L$$LIB_DIR -lQGLViewer

  macx {
    LIBS *= -lobjc
    CONFIG -= thread
  }

  # Remove debugging options
  QMAKE_CFLAGS_RELEASE -= -g
  QMAKE_CXXFLAGS_RELEASE -= -g

  !exists( $$(QTDIR)/lib/libqt-mt.* ) {
    exists( $$(QTDIR)/lib/libqt.* ) {
      CONFIG -= thread
      message( Using Qt non threaded version ) 
    }
  }
}


# Windows configuration.
# See doc/download.html page for details on include and lib paths.
win32 {
  # Various compilation flags
  QMAKE_CXXFLAGS = -TP -G6 -W1 -GR -GX -Zi
  # Optimise for speed, and expand any suitable inlines
  QMAKE_CXXFLAGS_RELEASE = -O2 -Ob2

  # Use the Qt DLL version
  DEFINES *= QT_DLL QT_THREAD_SUPPORT

  # Standard zip architechture : libQGLViewer-1.3.6 is ../../
  exists( ../../QGLViewer/qglviewer.h ) {
    INCLUDEPATH *= ../../
  }

  exists( ../../QGLViewer/Debug/QGLViewer*.lib ) {
    LIBPATH = ../../QGLViewer/Debug
  }

  exists( ../../QGLViewer/Release/QGLViewer*.lib ) {
    LIBPATH = ../../QGLViewer/Release
  }

  exists( ../../QGLViewer/QGLViewer*.lib ) {
    LIBPATH = ../../QGLViewer
  }

  win32-msvc.net {
    LIBS *= $$LIBPATH/QGLViewer138.lib
  } else {
    LIBS *= $$LIBPATH/QGLViewer.lib
  }
}
