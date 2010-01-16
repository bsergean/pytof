from __future__ import with_statement
import re
import ply.lex as lex
import ply.yacc as yacc

# import simplejson as json
# print json.dumps(tree, sort_keys=True, indent=4)

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
    'NAME', 'FLOAT',
    )

# Tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME   = r'\w+'
t_FLOAT  = r'\d+\.\d+'

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
# def p_main(p):
#     '''main : tree'''
#     global the_ast
#     the_ast = p[1]
    
def p_tree(p):
    '''tree : LPAREN FLOAT RPAREN
            | LPAREN FLOAT NAME tree tree RPAREN '''
    if len(p) == 4:
        p[0] = ( float(p[2]) )
    else:
        p[0] = ( float(p[2]), p[3], p[4], p[5] )

def p_error(p):
    print "Syntax error at '%s'" % p.value

def do_lex():
    # Build the lexer
    lex.lex()
    return

    lex.input(sometext)
    while 1:
        tok = lex.token()
        if not tok: break
        print tok

def do_yacc(sometext):
    yacc.yacc()
    return (yacc.parse(sometext), )

def do_parse(sometext):
    do_lex()
    return do_yacc(sometext)

def sln_input():
    return open('only_tree').read()
        
if __name__ == '__main__':
    sometext = sln_input()
    print do_parse(sometext)
