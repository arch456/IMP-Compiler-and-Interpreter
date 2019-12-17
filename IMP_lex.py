# Lexer for IMP language

from ply import lex

reserved = {
    'get'   : 'GET',
    'put'   : 'PUT',
    'if'    : 'IF',
    'else'  : 'ELSE',
    'while' : 'WHILE',
    'then'  : 'THEN',
    'end'   : 'END' ,
    'do'    : 'DO'
}

literals = [';',':','=','(',')','{','}','!']

tokens = [
          'PLUS','MINUS','TIMES','DIVIDE','EQ','NE','LT','GT','LE','GE','AND','OR','NOT','INT','ID','BOOL','ASSIGN'
          ] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ      = r'=='
t_NE      = r'!='
t_LT      = r'<'
t_GT      = r'>'
t_LE      = r'<='
t_GE      = r'>='
t_AND     = r'&&'
t_OR      = r'or'
t_NOT     = r'\!'
t_ASSIGN  = r':='

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_INT(t):
    r'[0-9]+'
    return t

def t_BOOL(t):
    r'[0|1]'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_NEWLINE(t):
    r'\n'
    pass

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex(debug=0)







       
   
  
            






