from __future__ import with_statement
import re
import simplejson as json

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

tokens = (
    'LPAREN','RPAREN',
    'NAME', 'FLOAT', 'INT',
    )

# Tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME   = r'\w+'
t_FLOAT  = r'\d+\.\d+'
t_INT    = r'\d+'

# Ignored characters
# t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    if lex_verbose: print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

###
#  YACC
###
def p_main(p):
    '''main : INT test_case_group'''
    global the_ast
    the_ast = p[2]
    
def p_test_case_group(p):
    '''test_case_group : test_case test_case_group
                       | test_case'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_test_case(p):
    '''test_case : INT tree INT animal_group'''
    pass

def p_tree(p):
    '''tree : LPAREN FLOAT RPAREN
            | LPAREN FLOAT NAME tree tree RPAREN '''
    if len(p) == 4:
        p[0] = ( p[2] )
    else:
        p[0] = ( p[2], p[3], p[4], p[5] )

def p_animal_group(p):
    '''animal_group : animal
                    | animal animal_group'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_animal(p):
    '''animal : animal_header feature_group
              | animal_header'''
    p[0] = p[1] + p[2] + p[3]

def p_animal_header(p):
    '''animal_header : NAME INT'''
    p[0] = p[1] + p[2]

def p_feature_group(p):
    '''feature_group : feature feature_group
                     | feature'''
    print len(p)
    print 'foo:', p[0]
    if len(p) == 2: print 'bar:', p[1]
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_feature(p):
    '''feature : NAME'''
    p[0] = p[1]

def p_error(p):
    print "Syntax error at '%s'" % p.value

def do_lex():
    # Build the lexer
    import ply.lex as lex
    lex.lex()
    return

    lex.input(sometext)
    while 1:
        tok = lex.token()
        if not tok: break
        print tok

def do_yacc():
    import ply.yacc as yacc
    yacc.yacc()
    yacc.parse(sometext)

def process_ast():
    tree = the_ast

    print json.dumps(tree, sort_keys=True, indent=4)

def do_parse():
    do_lex()
    do_yacc()
    # process_ast()

def sln_input():
    # return open('only_tree').read()
    return open('in').read()
        
animals = {}
# sometext = sln_input()
# do_parse()


def read_tree(text):
    p = re.compile('([a-z]+)')
    def tree_repl(match):
        return ",'%s'," % (match.groups()[0])
    text = p.sub(tree_repl, text)
    text = text.replace(')', '),')

    tree = eval(text)
    return tree

with open('in') as f:
    lines = f.read().splitlines()

nb_cases = int(lines[0])

ln = 1
for c in xrange(nb_cases):
    tree_len = int(lines[ln])
    ln += 1
    print tree_len

    tree_text = lines[ln:ln+tree_len]
    ln += tree_len
    print 'tree_text:', read_tree('\n'.join(tree_text))

    nb_animal = int(lines[ln])
    ln += 1
    print 'nb_animal:', nb_animal

    animals = lines[ln:ln+nb_animal]
    ln += nb_animal
    print animals
    

