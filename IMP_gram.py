# Grammar for IMP language

from ply import yacc
from IMP_lex import tokens, lexer

# define the precedence and associativity for the language here
precedence = (('left', 'AND', 'OR'),
              ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS', 'NOT')
             )

# define the grammar for IMP language
def p_grammar(_):
    '''
    program : stmt_list
    
    stmt_list : stmt stmt_list
              | empty

    stmt : block
         | ID ASSIGN aexp ';'
         | GET ID ';'
         | PUT exp ';'      
         | IF '(' bexp ')' THEN block opt_else END
         | WHILE '(' bexp ')' DO block END

    opt_else : ELSE block
             | empty
             
    block : '{' stmt_list '}'
          | empty
          
    exp : '(' exp ')'
        | aexp
        | bexp
        
    bexp : BOOL
         | aexp EQ aexp
         | aexp NE aexp
         | aexp LT aexp
         | aexp GT aexp
         | aexp LE aexp
         | aexp GE aexp
         | NOT bexp
         | bexp AND bexp
         | bexp OR bexp
         
    aexp : INT
         | ID
         | aexp PLUS aexp
         | aexp MINUS aexp
         | aexp TIMES aexp
         | aexp DIVIDE aexp
         | MINUS aexp %prec UMINUS

    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

### build the parser
parser = yacc.yacc()




 