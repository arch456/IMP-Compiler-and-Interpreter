# A tree walker that can interpret IMP language programs

from IMP_state import state
from grammar_stuff import assert_match

# defining functions for each node type

def seq(node):
    
    (SEQ, stmt, stmt_list) = node
    assert_match(SEQ, 'seq')
    
    walk(stmt)
    walk(stmt_list)


def nil(node):
    
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    # empty node, so we do nothing
    pass


def assign_stmt(node):

    (ASSIGNMENT, name, exp) = node
    assert_match(ASSIGNMENT, 'assign')
    
    value = walk(exp)
    state.symbol_table[name] = value

    
def block_stmt(node):
    
    (BLOCK, stmt_list) = node
    assert_match(BLOCK, 'block')
    
    walk(stmt_list)    
    

def get_stmt(node):

    (GET, name) = node
    assert_match(GET, 'get')

    s = input("Value for " + name + '? ')
    
    try:
        value = int(s)
    except ValueError:
        raise ValueError("expected an integer value for " + name)
    
    state.symbol_table[name] = value


def put_stmt(node):

    (PUT, exp) = node
    assert_match(PUT, 'put')
    
    value = walk(exp)
    print("> {}".format(value))


def while_stmt(node):

    (WHILE, cond, body) = node
    assert_match(WHILE, 'while')
    
    value = walk(cond)
    while value != 0:
        walk(body)
        value = walk(cond)


def if_stmt(node):
    
    try: # try the if-then pattern
        (IF, cond, then_stmt, (NIL,)) = node
        assert_match(IF, 'if')
        assert_match(NIL, 'nil')

    except ValueError: # if-then pattern didn't match
        (IF, cond, then_stmt, else_stmt) = node
        assert_match(IF, 'if')

        value = walk(cond)
        if value != 0:
            walk(then_stmt)
        else:
            walk(else_stmt)
        return
 
    else: # if-then pattern matched
        value = walk(cond)
        if value != 0:
            walk(then_stmt)
        return

    
def eq_exp(node):
    
    (EQ,c1,c2) = node
    assert_match(EQ, '==')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 == v2 else 0


def ne_exp(node):
    
    (NE,c1,c2) = node
    assert_match(NE, '!=')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 != v2 else 0


def lt_exp(node):
    
    (LT,c1,c2) = node
    assert_match(LT, '<')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 < v2 else 0


def gt_exp(node):
    
    (GT,c1,c2) = node
    assert_match(GT, '>')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 > v2 else 0


def le_exp(node):
    
    (LE,c1,c2) = node
    assert_match(LE, '<=')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 <= v2 else 0


def ge_exp(node):
    
    (GE,c1,c2) = node
    assert_match(GE, '>=')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 >= v2 else 0


def and_exp(node):
    
    (AND,c1,c2) = node
    assert_match(AND, '&&')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 and v2 else 0


def or_exp(node):
    
    (OR,c1,c2) = node
    assert_match(OR, 'or')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 or v2 else 0


def not_bexp(node):
    
    (NOT, bexp) = node
    assert_match(NOT, 'not')
    
    val = walk(bexp)
    return 0 if val != 0 else 1


def plus_exp(node):
    
    (PLUS,c1,c2) = node
    assert_match(PLUS, '+')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 + v2


def minus_exp(node):
    
    (MINUS,c1,c2) = node
    assert_match(MINUS, '-')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 - v2


def times_exp(node):
    
    (TIMES,c1,c2) = node
    assert_match(TIMES, '*')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 * v2


def divide_exp(node):
    
    (DIVIDE,c1,c2) = node
    assert_match(DIVIDE, '/')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 // v2


def bool_exp(node):

    (BOOL, value) = node
    assert_match(BOOL, 'boolean')
    
    return value


def integer_exp(node):

    (INT, value) = node
    assert_match(INT, 'integer')
    
    return value


def id_exp(node):
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    return state.symbol_table.get(name, 0)


def uminus_exp(node):
    
    (UMINUS, aexp) = node
    assert_match(UMINUS, 'uminus')
    
    val = walk(aexp)
    return - val


def paren_exp(node):
    
    (PAREN, exp) = node
    assert_match(PAREN, 'paren')
    
    # return the value of the parenthesized expression
    return walk(exp)


# walk

def walk(node):
    # node format: (TYPE, [child1[, child2[, ...]]])
    type = node[0]
    
    if type in dispatch_dict:
        node_function = dispatch_dict[type]
        return node_function(node)
    else:
        raise ValueError("walk: unknown tree node type: " + type)

# a dictionary to associate tree nodes with node functions
dispatch_dict = {
    'seq'     : seq,
    'nil'     : nil,
    'assign'  : assign_stmt,
    'get'     : get_stmt,
    'put'     : put_stmt,
    'while'   : while_stmt,
    'if'      : if_stmt,
    'block'   : block_stmt,
    'integer' : integer_exp,
    'boolean' : bool_exp,
    'id'      : id_exp,
    'paren'   : paren_exp,
    '+'       : plus_exp,
    '-'       : minus_exp,
    '*'       : times_exp,
    '/'       : divide_exp,
    '=='      : eq_exp,
    '!='      : ne_exp,
    '<'       : lt_exp,
    '>'       : gt_exp,
    '<='      : le_exp,
    '>='      : ge_exp,
    '&&'      : and_exp,
    'or'      : or_exp,
    'uminus'  : uminus_exp,
    'not'     : not_bexp
}


