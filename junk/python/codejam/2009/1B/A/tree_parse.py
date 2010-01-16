from __future__ import with_statement
import re
import sys
import simplejson as json
from pdb import set_trace

# Doc: http://www.dabeaz.com/ply/ply.html
# Complicated example: http://code.google.com/p/pycparser/source/browse/trunk/pycparser/c_parser.py
lex_verbose = False

'''
(0.2 furry
  (0.81 fast
    (0.3)
    (0.2)
  )
  (0.1 fishy
    (0.3 freshwater
      (0.01)
      (0.01)
    )
    (0.1)
  )
)

tree ::= (weight [feature tree tree])
weight is a real number between 0 and 1, inclusive
feature is a string of 1 or more lower case English letters
'''

def read_tree(text):
    p = re.compile('([a-z]+)')
    def tree_repl(match):
        return ",'%s'," % (match.groups()[0])
    text = p.sub(tree_repl, text)
    text = text.replace(')', '),')

    if False:
        tree = eval(text)
    else:
        # Does not work, not sure it's as easy as I thought
        # (], is not allowed while ), is allowed as a tuple
        p = re.compile('(\d+\.\d+)+')
        def tree_repl(match):
            return "'%s'" % (match.groups()[0])
        text = p.sub(tree_repl, text)

        text = text.replace(')', ']')
        text = text.replace('(', '[')

        import simplejson as json
        print text
        tree = json.loads(text)
    return tree

import types
def is_float(f):
    return type(f) == types.FloatType

def process(tree, animal_feats):
    if is_float(tree):
        return tree
    else:
        ratio = tree[0]
        feature = tree[1]
        if feature in animal_feats:
            return ratio * process( tree[2], animal_feats)
        else: 
            return ratio * process( tree[3], animal_feats)

with open('in') as f:
    lines = f.read().splitlines()

nb_cases = int(lines[0])

ln = 1
case = 1
out = ''

# Need that for big file, eval does blow out of memory (MemoryError)
# We could also print to a file and import it but it's not
# as clean as parsing it.
from tree_parse_ply import do_parse as read_tree

for c in xrange(nb_cases):
    tree_len = int(lines[ln])
    ln += 1
    print tree_len

    tree_text = lines[ln:ln+tree_len]
    ln += tree_len
    tree = read_tree('\n'.join(tree_text))
    print 'tree_text:', tree

    nb_animal = int(lines[ln])
    ln += 1
    print 'nb_animal:', nb_animal

    animals_text = lines[ln:ln+nb_animal]
    ln += nb_animal
    print animals_text

    out += 'Case #%d:\n' % (c+1)
    for a in animals_text:
        tokens = a.split()
        name = tokens[0]
        features = tokens[2:]
        proba = process(tree[0], features)
        print name+':', proba
        out += '%.7f\n' % proba

sys.stderr.write(out)
    

