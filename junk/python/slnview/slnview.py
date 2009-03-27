# Doc: http://www.dabeaz.com/ply/ply.html
lex_verbose = False

def sln_input():
    input = 'simple'
    input = 'project'
    input = 'global'
    input = 'nested'
    input = 'platforms'
    input = 'simple_complete'
    input = 'a3d'
    return open(input + '.sln').read()
        
sometext = sln_input()

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
    'PROJECTCONFIGURATIONPLATFORMS',  'POSTSOLUTION', 'SOLUTIONPROPERTIES',
    'WIN32', 'X64', 'ACTIVECONFIG', 'BUILD0', 'FLOAT'
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
t_PRESOLUTION         = r'preSolution'
t_POSTSOLUTION        = r'postSolution'
t_POSTPROJECT         = r'postProject'
t_NESTEDPROJECTS      = r'NestedProjects'
t_SOLUTIONPROPERTIES  = r'SolutionProperties'
t_WIN32               = r'Win32'
t_X64                 = r'x64'
t_ACTIVECONFIG        = r'ActiveCfg'
t_BUILD0              = r'Build.0'
t_VCPROJPATH          = r'[\w\\.]+.vcproj' # Don't need to escape \
t_CONF                = r'\w[\w \-]+\|'
t_NAME                = r'\w+'
t_GUID                = r'\{{0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}\}'
t_SOLUTIONCONFIGURATIONPLATFORMS = 'SolutionConfigurationPlatforms'
t_PROJECTCONFIGURATIONPLATFORMS  = 'ProjectConfigurationPlatforms'
t_FLOAT               = r'\d+\.\d+'

# Ignored characters
# t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

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
def p_main_file(t):
    'main_file : header main_statement_group'

# Cannot Use lex to take the long string below as a single lex token
# Microsoft Visual Studio Solution File, Format Version 9.00
# 1         2      3      4        5   , 6      7
def p_header(t):
    'header : NAME NAME NAME NAME NAME COMMA NAME NAME FLOAT'

def p_main_statement_group(t):
    '''main_statement_group : main_statement main_statement_group
                            | main_statement'''

def p_main_statement(t):
    '''main_statement : PROJECT project_statement
                      | GLOBAL  global_statement'''

def p_project_statement(t):
    '''project_statement : LPAREN quoted RPAREN project_3_uple project_section ENDPROJECT
                         | LPAREN quoted RPAREN project_3_uple ENDPROJECT'''

def p_project_section(t):
    'project_section : PROJECTSECTION LPAREN PROJECTDEPENDENCIES RPAREN project_section_body ENDPROJECTSECTION'

def p_project_section_body(t):
    'project_section_body : EQUALS POSTPROJECT post_project_list'

def p_post_project_list(t):
    '''post_project_list : GUID EQUALS GUID post_project_list
                         | GUID EQUALS GUID '''
    print t[1], t[3]
    
def p_project_3_uple(t):
    'project_3_uple : EQUALS quoted COMMA quoted COMMA quoted'

def p_quoted(t):
    'quoted : DOUBLEQUOTE expr DOUBLEQUOTE'

def p_expr(t):
    '''expr : GUID
            | name_list
            | VCPROJPATH'''
    print 'Expr', t[1]

def p_name_list(t):
    '''name_list : NAME name_list
                 | NAME'''

###
#  GLOBAL
### 
def p_global_statement(t):
    'global_statement : globalsection_statement_group ENDGLOBAL'

def p_global_statement_group(t):
    '''globalsection_statement_group : GLOBALSECTION globalsection_statement ENDGLOBALSECTION globalsection_statement_group
                                     | GLOBALSECTION globalsection_statement ENDGLOBALSECTION '''

def p_globalsection_statement(t):
    '''globalsection_statement : LPAREN SOLUTIONCONFIGURATIONPLATFORMS RPAREN solution_conf_body
                               | LPAREN PROJECTCONFIGURATIONPLATFORMS RPAREN project_conf_body
                               | LPAREN SOLUTIONPROPERTIES RPAREN properties_body
                               | LPAREN NESTEDPROJECTS RPAREN nested_body'''

def p_solution_conf_body(t):
    'solution_conf_body : EQUALS PRESOLUTION solution_conf_list'

def p_pre_solution_list(t):
    '''solution_conf_list : CONF arch EQUALS CONF arch solution_conf_list
                          | CONF arch EQUALS CONF arch '''
    print t[1]
    return
    for i,e in enumerate(t):
        print 'pre_solution_list', i, e

def p_arch(t):
    '''arch : WIN32
            | X64'''

def p_project_conf_body(t):
    'project_conf_body : EQUALS POSTSOLUTION project_conf_list'

def p_project_conf_list(t):
    '''project_conf_list : GUID DOT CONF arch DOT build_conf EQUALS CONF arch project_conf_list
                         | GUID DOT CONF arch DOT build_conf EQUALS CONF arch '''
    print t[1], t[3], t[7]
    return
    for i,e in enumerate(t):
        print 'pre_solution_list', i, e

def p_build_conf(t):
    '''build_conf : ACTIVECONFIG
                  | BUILD0'''

def p_properties_body(t):
    'properties_body : EQUALS PRESOLUTION properties_list'

def p_properties_list(t):
    '''properties_list : NAME EQUALS NAME properties_list
                       | NAME EQUALS NAME'''

def p_nested_body(t):
    'nested_body : EQUALS PRESOLUTION nested_body_list'

def p_nested_body_list(t):
    '''nested_body_list : GUID EQUALS GUID nested_body_list
                        | GUID EQUALS GUID '''
    print t[1], t[3]

def p_error(t):
    print "Syntax error at '%s'" % t.value

import ply.yacc as yacc
yacc.yacc()

yacc.parse(sometext)

