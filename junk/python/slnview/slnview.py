# Doc: http://www.dabeaz.com/ply/ply.html
# Complicated example: http://code.google.com/p/pycparser/source/browse/trunk/pycparser/c_parser.py
lex_verbose = False

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

# YACC
# Node class not used for now.
import types # types.ListType
class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf

    def rec_print(self, t, spaces = ''):
        print spaces, t.type, t.leaf
        for b in t.children:
            self.rec_print(b, spaces + ' ')

    def do_print(self):
        self.rec_print(self)

# TODO: project_section is optional
def p_main_file(p):
    'main_file : header main_statement_group'
    global the_ast
    the_ast = [p[1], p[2]]

# Cannot Use lex to take the long string below as a single lex token
# Microsoft Visual Studio Solution File, Format Version 9.00
# 1         2      3      4        5   , 6      7
def p_header(p):
    'header : NAME NAME NAME NAME NAME COMMA NAME NAME FLOAT'
    p[0] = p[9]

def p_main_statement_group(p):
    '''main_statement_group : main_statement main_statement_group
                            | main_statement'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_main_statement(p):
    '''main_statement : PROJECT project_statement
                      | GLOBAL  global_statement'''
    p[0] = p[2]

def p_project_statement(p):
    '''project_statement : project_declaration project_section ENDPROJECT
                         | project_declaration ENDPROJECT'''
    if len(p) == 4:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1]]

def p_project_declaration(p):
    'project_declaration : LPAREN quoted RPAREN project_3_uple'
    p[0] = [p[2], p[4]]

def p_project_section(p):
    'project_section : PROJECTSECTION LPAREN PROJECTDEPENDENCIES RPAREN project_section_body ENDPROJECTSECTION'
    p[0] = p[5]

def p_project_section_body(p):
    'project_section_body : EQUALS POSTPROJECT post_project_list'
    p[0] = p[3]

def p_post_project_list(p):
    '''post_project_list : post_project_core post_project_list
                         | post_project_core '''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_post_project_core(p):
    'post_project_core : GUID EQUALS GUID'
    p[0] = [p[1], p[3]]
    
def p_project_3_uple(p):
    'project_3_uple : EQUALS quoted COMMA quoted COMMA quoted'
    p[0] = [p[2], p[4], p[6]]

def p_quoted(p):
    'quoted : DOUBLEQUOTE expr DOUBLEQUOTE'
    p[0] = p[2]

def p_expr(p):
    '''expr : GUID
            | name_list
            | VCPROJPATH'''
    p[0] = p[1]

def p_name_list(p):
    '''name_list : NAME name_list
                 | NAME'''
    p1 = [p[1]] # needs that because NAME is a string and 
                # concat list + string does not work
    p[0] = p1 if len(p) == 2 else p1 + p[2]

###
#  GLOBAL
### 
def p_global_statement(p):
    'global_statement : globalsection_statement_group ENDGLOBAL'
    p[0] = p[1]

def p_global_statement_group(p):
    '''globalsection_statement_group : GLOBALSECTION globalsection_statement ENDGLOBALSECTION globalsection_statement_group
                                     | GLOBALSECTION globalsection_statement ENDGLOBALSECTION '''
    p[0] = [p[2]] if len(p) == 4 else p[2] + p[4]

def p_globalsection_statement(p):
    '''globalsection_statement : LPAREN SOLUTIONCONFIGURATIONPLATFORMS RPAREN solution_conf_body
                               | LPAREN PROJECTCONFIGURATIONPLATFORMS RPAREN project_conf_body
                               | LPAREN SOLUTIONPROPERTIES RPAREN properties_body
                               | LPAREN NESTEDPROJECTS RPAREN nested_body'''
    p[0] = p[4] # FIXME

def p_solution_conf_body(p):
    'solution_conf_body : EQUALS PRESOLUTION solution_conf_list'
    p[0] = p[3]

def p_pre_solution_list(p):
    '''solution_conf_list : pre_solution_core solution_conf_list
                          | pre_solution_core '''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_pre_solution_core(p):
    'pre_solution_core : CONF arch EQUALS CONF arch'
    p[0] = [p[1], p[2], p[4], p[5]]

def p_arch(p):
    '''arch : WIN32
            | X64'''
    p[0] = p[1]

def p_project_conf_body(p):
    'project_conf_body : EQUALS POSTSOLUTION project_conf_list'
    p[0] = p[3]

def p_project_conf_list(p):
    '''project_conf_list : project_conf_core project_conf_list
                         | project_conf_core'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_project_conf_core(p):
    'project_conf_core : GUID DOT CONF arch DOT build_conf EQUALS CONF arch'
    p[0] = [p[1], p[3], p[7], p[5]] # FIXME
    return
    for i,e in enumerate(p):
        print 'pre_solution_list', i, e

def p_build_conf(p):
    '''build_conf : ACTIVECONFIG
                  | BUILD0'''
    p[0] = p[1]

def p_properties_body(p):
    'properties_body : EQUALS PRESOLUTION properties_list'
    p[0] = p[3]

def p_properties_list(p):
    '''properties_list : properties_core properties_list
                       | properties_core'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_properties_core(p):
    'properties_core : NAME EQUALS NAME'
    p[0] = [p[1], p[3]]

def p_nested_body(p):
    'nested_body : EQUALS PRESOLUTION nested_body_list'
    p[0] = p[3]

def p_nested_body_list(p):
    '''nested_body_list : nested_body_core nested_body_list
                        | nested_body_core '''
    p[0] = [p[1]] if len(p) == 2 else p[1] + p[2]

def p_nested_body_core(p):
    'nested_body_core : GUID EQUALS GUID'
    p[0] = [p[1], p[3]]

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

def do_parse():
    do_lex()
    do_yacc()
    process_ast()

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

def process_ast():
    version = the_ast[0]
    print 'version:', version
    pass #for 

