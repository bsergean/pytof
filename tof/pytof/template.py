"""
Simple templating engine, front-end to ezt.py
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id: options.py 294 2007-03-12 04:28:19Z bsergean $  (C) 2007 GPL'

from log import logger
from os.path import join, exists, splitext, basename
import os, sys
from utils import ListCurrentDirFileFromExt

class TemplateError(Exception): pass
class pytofTemplate(object):

    templateDir = join(sys.prefix, 'share', 'pytof', 'templates')
    styleDir = join(sys.prefix, 'share', 'pytof', 'styles')

    def __init__(self):
	# styles:
	self.styles = []
	for fStyle in ListCurrentDirFileFromExt('.css', self.styleDir):
	    style = splitext(basename(fStyle))[0] # get rid of the ext

	    # FIXME: this is to workaround a bug with non case sensitive
	    # filesystems (Mac and Windoze). Should be fixed in ListCurrentDirFileFromExt
	    if not style in self.styles:
		templates = ['_photo_per_page.ezt', '_gallery_index.ezt', '_main_index.ezt']
		templates = [join(self.templateDir, style + t) for t in templates]

		if map(exists, templates) == [True for t in templates]:
		    self.styles.append(style)

    def write(self, pagetype, data, output, style = 'scry'):
	from ezt import Template

	# FIXME: Great error handling
	styles = ['scry', 'james']
	pageTypes = {'photo': '_photo_per_page.ezt',
		     'index': '_gallery_index.ezt',
		     'main': '_main_index.ezt'}

	# FIXME:
	if not style in styles:
	    raise TemplateError, '%s is not a supported style' % style

	css_content = open(join(self.styleDir, style + '.css')).read()
	data['css_content'] = css_content

	template = join(self.templateDir, style + pageTypes[pagetype])
	pytofTemplate = Template(template)
	wfile = open(output, 'w')
	pytofTemplate.generate(wfile, data)
