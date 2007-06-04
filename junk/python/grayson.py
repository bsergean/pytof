from sgmllib import SGMLParser
import sys

class sgmlElementsCounter(SGMLParser):
	"""
	Nice and Slow
	
	[bsergean@marge1 grayson]$ time python grayson.py
	601261
	Command exited with non-zero status 1
	288.25user 7.48system 5:03.75elapsed 97%CPU (0avgtext+0avgdata 0maxresident)k
	0inputs+0outputs (0major+44981minor)pagefaults 0swaps
	"""
	def reset(self):
		SGMLParser.reset(self)
		self.elements = 0

	def start_entry(self, attrs):
		self.elements += 1

class simpleElementsCounter:
	"""
	Fast and furious (and ugly)
	
	[bsergean@marge1 grayson]$ time python grayson.py
	601261
	Command exited with non-zero status 1
	6.92user 1.03system 0:08.10elapsed 98%CPU (0avgtext+0avgdata 0maxresident)k
	0inputs+0outputs (0major+108817minor)pagefaults 0swaps
	"""
	
	def __init__(self, fo):
		i = 0
		for l in fo.readlines():
			if l.find('entry') != -1:
				i += 1
		self.elements = i / 2

class ProgressMsg(object):
	""" General purpose progress bar """
	def __init__(self, target, output=sys.stdout):
		self.output = output
		self.counter = 0
		self.target = target
		
	def Increment(self):
		if self.counter == 0:
			self.output.write("\n")
		self.counter += 1
		msg = "\r%.0f%% - (%d processed out of %d) " \
		      % (100 * self.counter / float(self.target), self.counter, self.target)
		self.output.write(msg)
		self.output.flush()
		if self.counter == self.target:
			self.output.write("\n")

class txtParser(SGMLParser):
	"""
	[bsergean@marge1 grayson]$ time python grayson.py > result.txt
	Computing number of elements to process...
	
	100% - (601261 processed out of 601261)
	290.73user 10.75system 5:29.56elapsed 91%CPU (0avgtext+0avgdata 0maxresident)k
	0inputs+0outputs (0major+162794minor)pagefaults 0swaps	
	"""
	def reset(self):
		SGMLParser.reset(self)
		self.entries = {}

	def init(self, nbElements):
		self.progress = ProgressMsg(nbElements, sys.stderr)

	def start_entry(self, attrs):
		self.entryID = attrs[0][1]
		self.listValues = []
		self.progress.Increment()
		
	def end_entry(self):
		self.entries[self.entryID] = self.listValues

	# disc (1 to 4)
	def start_disc1(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_disc2(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_disc3(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_disc4(self, attrs):
		self.listValues.append(attrs[0][1])

	# sound (1 to 6)
	def start_sound1(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_sound2(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_sound3(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_sound4(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_sound5(self, attrs):
		self.listValues.append(attrs[0][1])
	def start_sound6(self, attrs):
		self.listValues.append(attrs[0][1])


try:
	fo = open('data.txt')
	#fo = open('data_simple.txt')

	xml = False
	sys.stderr.write('Computing number of elements to process...\n')
	if xml:
		elemsParser = sgmlElementsCounter()
		elemsParser.feed(fo.read())
	else:
		elemsParser = simpleElementsCounter(fo)

	parser = txtParser()
	parser.init(elemsParser.elements)
	fo.seek(0)
	parser.feed(fo.read())

	keys = map(int, parser.entries.keys())
	keys.sort()
	for key in keys:
		print '%s,%s' %(key, (':').join(parser.entries[str(key)]))

	parser.close()
except (KeyboardInterrupt):
	print '\nInterrupted by user'

