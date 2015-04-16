"""
Simple logger module based on the standard module logging (needs python 2.3).
"""

# Copyright (C) 2006, 2007 GPL
# Written by Mathieu Robin <mathieu.robin@gmail.com> and by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

import logging

# TODO: Would be nice to have funcName here as well, but it's only available for python >- 2.5
format = "%(levelname)s\t[%(pathname)s:%(lineno)d] %(message)s"

# Create logger
logger = logging.getLogger('pytof')
logger.setLevel(logging.DEBUG)

# Create handler and set level to debug
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(format))

# Add handler to the main logger instance
logger.addHandler(handler)

def quiet():
    logger.setLevel(logging.WARNING)
