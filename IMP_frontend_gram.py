# Specification of the Frontend for the IMP language

from ply import yacc
from IMP_lex import tokens, lexer
from IMP_state import state

# define the precedence and associativity for the language here
precedence = (('left', 'AND', 'OR'),
              ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS', 'NOT')
             )

# We specify the rules of the IMP grammar rules, with their corresponding actions

def p_prog(p):
    '''
    program : stmt_list
    '''
    state.AST = p[1]

def p_stmt_list(p):
    '''
    stmt_list : stmt stmt_list
              | empty
    '''
    if (len(p) == 3):
        p[0] = ('seq', p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_stmt(p):
    '''
    stmt : block
         | GET ID ';'
         | PUT exp ';'      
         | IF '(' bexp ')' THEN block opt_else END
         | WHILE '(' bexp ')' DO block END
    '''
    if (len(p) == 1):
        p[0] = p[1]
    elif p[1] == 'get':
        p[0] = ('get', p[2])
        state.symbol_table[p[2]] = None
    elif p[1] == 'put':
        p[0] = ('put', p[2])
    elif p[1] == 'if':
        p[0] = ('if', p[3], p[6], p[7])
    elif p[1] == 'while':
        p[0] = ('while', p[3], p[6])
    else:
        raise ValueError("unexpected symbol {}".format(p[1]))

def p_assign(p):
    '''
    stmt : ID ASSIGN aexp ';'
    '''
    p[0] = ('assign', p[1], p[3])
    state.symbol_table[p[1]] = None
        
def p_opt_else(p):
    '''
    opt_else : ELSE block
             | empty
    '''
    if p[1] == 'else':
        p[0] = p[2]
    else:
        p[0] = p[1]
    
def p_block(p):
    '''
    block : '{' stmt_list '}'
    '''      
    p[0] = ('block',p[2])
        
def p_exp(p):
    '''
    exp : aexp
        | bexp
    '''      
    p[0] = p[1]

def p_paren_exp(p):
    '''
    exp : '(' exp ')'
    '''
    p[0] = ('paren', p[2])

def p_bool_bexp(p):
    '''
    bexp : BOOL
    '''
    p[0] = p[1]
    
def p_bexp(p):
    '''
    bexp : aexp EQ aexp
         | aexp NE aexp
         | aexp LT aexp
         | aexp GT aexp
         | aexp LE aexp
         | aexp GE aexp
         | bexp AND bexp
         | bexp OR bexp
    '''
    p[0] = (p[2], p[1], p[3])
        
def p_not_bexp(p):
    '''
    bexp : NOT bexp
    '''
    p[0] = ('not', p[2])

def p_aexp(p):
    '''
    aexp : aexp PLUS aexp
         | aexp MINUS aexp
         | aexp TIMES aexp
         | aexp DIVIDE aexp
    '''     
    p[0] = (p[2], p[1], p[3])

def p_integer_aexp(p):
    '''
    aexp : INT
    '''
    p[0] = ('integer', int(p[1]))
    
def p_id_aexp(p):
    '''
    aexp : ID
    '''
    p[0] = ('id', p[1])

def p_uminus_aexp(p):
    '''
    aexp : MINUS aexp %prec UMINUS
    '''
    p[0] = ('uminus', p[2])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = ('nil',)

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    
# build the parser
parser = yacc.yacc(debug=False,tabmodule='impparsetab')

