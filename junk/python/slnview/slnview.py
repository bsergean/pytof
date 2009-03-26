# Doc: http://www.dabeaz.com/ply/ply.html
lex_verbose = False

sln_input = {
        'simple': '\n'.join(open('simple.sln').read().splitlines()[2:]),
        'simple_complete': '\n'.join(open('simple_complete.sln').read().splitlines()[2:]),
        'full': '\n'.join(open('a3d.sln').read().splitlines()[2:]),
        'project': open('project.sln').read(),
        'global': open('global.sln').read(),
        'nested': open('nested.sln').read(),
        'platforms': open('platforms.sln').read(),
        }
sometext = sln_input['simple_complete']

tokens = (
    'NAME', 'CONF',
    'VCPROJPATH',
    'GUID', 'EQUALS',
    'LPAREN','RPAREN',
    'DOUBLEQUOTE','COMMA',
    'PROJECT', 'ENDPROJECT',
    'PROJECTSECTION', 'ENDPROJECTSECTION',
    'PROJECTDEPENDENCIES', 'POSTPROJECT',
    'GLOBAL', 'GLOBALSECTION', 'ENDGLOBAL', 'ENDGLOBALSECTION',
    'SOLUTIONCONFIGURATIONPLATFORMS', 'PRESOLUTION', 'DOT', 'NESTEDPROJECTS',
    'WIN32', 'X64', 'ACTIVECONFIG', 'BUILD0',
    )

# Tokens
t_DOT                 = r'\.'
t_EQUALS              = r'='
t_LPAREN              = r'\('
t_RPAREN              = r'\)'
t_DOUBLEQUOTE         = r'\"'
t_COMMA               = r','
t_PROJECT             = r'Project'
t_ENDPROJECT          = r'EndProject'
t_PROJECTSECTION      = r'ProjectSection'
t_ENDPROJECTSECTION   = r'EndProjectSection'
t_PROJECTDEPENDENCIES = r'ProjectDependencies'
t_GLOBAL              = r'Global'
t_GLOBALSECTION       = r'GlobalSection'
t_ENDGLOBAL           = r'EndGlobal'
t_ENDGLOBALSECTION    = r'EndGlobalSection'
t_SOLUTIONCONFIGURATIONPLATFORMS = 'SolutionConfigurationPlatforms'
t_PRESOLUTION         = r'preSolution'
t_POSTPROJECT         = r'postProject'
t_NESTEDPROJECTS      = r'NestedProjects'
t_WIN32               = r'Win32'
t_X64                 = r'x64'
t_ACTIVECONFIG        = r'ActiveCfg'
t_BUILD0              = r'Build.0'
t_VCPROJPATH          = r'[a-zA-Z0-9\\.]+.vcproj' # Don't need to escape \
t_CONF                = r'\w[\w \-]+\|'
t_NAME                = r'\w+'
t_GUID                = r'\{{0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}\}'

# t_GUID                = r'\{.*\}$'

# Ignored characters
# t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    if lex_verbose: print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    

# Build the lexer
import ply.lex as lex
lex.lex()

do_lex_only = False
if do_lex_only:
    lex.input(sometext)
    while 1:
        tok = lex.token()
        if not tok: break
        print tok

    import sys ; sys.exit(0)

# Parsing rules

if False:
    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('right','UMINUS'),
        )

# dictionary of names
names = { }

# TODO: project_section is optional
def p_main_statement_group(t):
    '''main_statement_group : main_statement main_statement_group
                            | main_statement'''
    pass

def p_main_statement(t):
    '''main_statement : PROJECT project_statement
                      | GLOBAL  global_statement'''
    pass

def p_project_statement(t):
    '''project_statement : LPAREN quoted RPAREN project_3_uple project_section ENDPROJECT
                         | LPAREN quoted RPAREN project_3_uple ENDPROJECT'''
    pass

def p_project_section(t):
    'project_section : PROJECTSECTION LPAREN PROJECTDEPENDENCIES RPAREN project_section_body ENDPROJECTSECTION'
    pass

def p_project_section_body(t):
    'project_section_body : EQUALS POSTPROJECT post_project_list'
    pass

def p_post_project_list(t):
    '''post_project_list : GUID EQUALS GUID post_project_list
                         | GUID EQUALS GUID '''
    print t[0], t[1], t[2], t[3]
    if len(t) == 5:
        print t[4] # it's None ...
    
def p_project_3_uple(t):
    'project_3_uple : EQUALS quoted COMMA quoted COMMA quoted'
    pass

def p_quoted(t):
    'quoted : DOUBLEQUOTE expr DOUBLEQUOTE'
    pass

def p_expr(t):
    '''expr : GUID
            | NAME
            | VCPROJPATH'''
    print 'Expr:', t[1]

###
#  GLOBAL
### 
def p_global_statement(t):
    '''global_statement : GLOBALSECTION globalsection_statement ENDGLOBALSECTION ENDGLOBAL
                        | ENDGLOBAL'''

def p_globalsection_statement(t):
    'globalsection_statement : LPAREN SOLUTIONCONFIGURATIONPLATFORMS RPAREN globalsection_body'

def p_globalsection_body(t):
    'globalsection_body : EQUALS PRESOLUTION pre_solution_list'

def p_pre_solution_list(t):
    '''pre_solution_list : CONF arch EQUALS CONF arch pre_solution_list
                         | CONF arch EQUALS CONF arch '''

def p_arch(t):
    '''arch : WIN32
            | X64'''

def p_error(t):
    print "Syntax error at '%s'" % t.value

import ply.yacc as yacc
yacc.yacc()

yacc.parse(sometext)

