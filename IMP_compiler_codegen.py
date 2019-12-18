from IMP_state import state
from grammar_stuff import assert_match

# This is the translated code generator for the IMP compiler
# The generated code is a list of JVM bytecode instructions for the corresponding statements in IMP

i = 0 # counter for the store instruction
j = 0 # counter for the load instruction
    
# node functions
def seq(node):

    global i,j 
    (SEQ, s1, s2) = node
    assert_match(SEQ, 'seq')
    
    stmt = walk(s1)
    lst = walk(s2)

    return stmt + lst

# Empty node
def nil(node):
    
    global i,j 
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    code = []
    i = 0         # reset the instruction counters
    j = 0
    return code
    

def assign_stmt(node):

    global i
    (ASSIGN, name, exp) = node
    assert_match(ASSIGN, 'assign')
    
    exp_code = walk(exp)
    state.symbol_table[name] = exp_code
    
    if isinstance(exp_code, list):
        code = exp_code
                
    else:
        val = state.symbol_table.get(name,0)
        code = [('iconst_'+val,)]
        code += [('istore_'+str(i),)]
        i+=1

    return code


def input_stmt(node):

    global i
    (INPUT, name) = node
    assert_match(INPUT, 'input')
    
    code = [('invokevirtual        java/util/Scanner.nextInt()I' ,)]    # bytecode for reading input 
    code += [('istore_'+str(i),)]
    i+=1
    
    return code


def print_stmt(node):

    (PRINT, exp) = node
    assert_match(PRINT, 'print')
    
    exp_code = walk(exp)

    code = [('invokevirtual        java/io/PrintStream.println:(Ljava/lang/String;)V',)]    # bytecode for a print statement
    
    return code


def while_stmt(node):
    
    (WHILE, cond, body) = node
    assert_match(WHILE, 'while')
    
    begin_label = label()
    true_label = label()
    false_label = label()
    
    cond_code = walk(cond)
    body_code = walk(body)
    
    code = [(begin_label + ':',)]
    code += cond_code
    code += cond_expr(cond[0],false_label)     
    
    code += [(true_label + ':',)]
    code += body_code
    code += [('goto\t'+begin_label,)]
    code += [(false_label + ':',)]
    code += [('end_while',)]

    return code

#########################################################################
def if_stmt(node):

    try: 
        (IF, cond, s1, (NIL,)) = node
        assert_match(IF, 'if')
        assert_match(NIL, 'nil')
    
    except ValueError:    # statement matches if-then-else pattern
        (IF, cond, s1, s2) = node
        assert_match(IF, 'if')
        
        false_label = label()
        cond_code = walk(cond)
        stmt1_code = walk(s1)
        stmt2_code = walk(s2)

        code = cond_expr(cond[0],false_label)
        code += cond_code   
        code += stmt1_code
        code += [('end_then',)]
        code += stmt2_code
        code += [(false_label + ':',)]
        code += [('end_if',)]

        return code

    else:    # statement matches if-then pattern
        false_label = label();
        cond_code = walk(cond)
        stmt1_code = walk(s1)
        
        code = cond_expr(cond[0],false_label)
        code += cond_code    
        code += stmt1_code
        code += [(false_label + ':',)]
        code += [('end_if',)]

        return code


def block_stmt(node):

    (BLOCK, s) = node
    assert_match(BLOCK, 'block')

    code = walk(s)
    
    return code


def arith_exp(node):   #for Arithmetic expressions

    global i,j 
    (OP, c1, c2) = node
    if OP not in ['+', '-', '*', '/']:
        raise ValueError("pattern match failed on " + OP)
    code = []
    
    lcode = walk(c1)
    rcode = walk(c2)

    # for each of the Arithmetic operations
    if OP == '+':
        code += [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('iadd',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP == '-':
        code += [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('isub',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP == '*':
        code += [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('imul',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP == '/':
        code += [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('idiv',)]
        code += [('istore_'+str(i),)]
        i+=1
 
    return code   


def rel_exp(node):   #for Relational expressions 
    
    global i,j 
    (OP, c1, c2) = node
    if OP not in ['==', '<=', '<', '>', '!=', '>=']:
        raise ValueError("pattern match failed on " + OP)
    code = []
    
    lcode = walk(c1)
    rcode = walk(c2)

    # for Relational operators
    if OP in ['<','>','==', '<=', '!=', '>=']:
        if c1[0] == 'id':
            code += [('iload_'+str(j),)]
            j+=1
        if c2[0] == 'id':
            code += [('iload_'+str(j),)] 
            j+=1
        if c1[0] == 'integer':
            code += [('iconst_'+lcode,)]
        if c2[0] == 'integer':
            code += [('iconst_'+rcode,)]
        
    return code


def integer_exp(node):

    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')

    return str(value)


def id_exp(node):
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    return name


def uminus_exp(node):
    
    (UMINUS, e) = node
    assert_match(UMINUS, 'uminus')
    
    code = walk(e)

    return '-' + code


def not_exp(node):
    
    (NOT, e) = node
    assert_match(NOT, 'not')
    
    code = walk(e)

    return '!' + code


def paren_exp(node):
    
    (PAREN, exp) = node
    assert_match(PAREN, 'paren')
    
    exp_code = walk(exp)

    return exp_code


def cond_expr(op,flabel): # this procedure returns the corresponding bytecode instruction for each type of condition
    
    code = []
    if op == '==':
        code += [('if_icmpne\t'+flabel,)]
    elif op == '!=':
        code += [('if_icmpeq\t'+flabel,)]
    elif op == '<':
        code += [('if_icmpge\t'+flabel,)]
    elif op == '>':
        code += [('if_icmple\t'+flabel,)]
    elif op == '<=':
        code += [('if_icmpgt\t'+flabel,)]
    elif op == '>=':
        code += [('if_icmplt\t'+flabel,)]
        
    return code

# function for the Abstract Syntaxt Tree walker

def walk(node):
    node_type = node[0]
    
    if node_type in dispatch_dict:
        node_function = dispatch_dict[node_type]
        return node_function(node)
    
    else:
        raise ValueError("walk: unknown tree node type: " + node_type)

# this dictionary combines each node with its corresponding function
dispatch_dict = {
    'seq'     : seq,
    'nil'     : nil,
    'assign'  : assign_stmt,
    'input'   : input_stmt,
    'print'   : print_stmt,
    'while'   : while_stmt,
    'if'      : if_stmt,
    'block'   : block_stmt,
    'integer' : integer_exp,
    'id'      : id_exp,
    'uminus'  : uminus_exp,
    'not'     : not_exp,
    'paren'   : paren_exp,
    '+'       : arith_exp,
    '-'       : arith_exp,
    '*'       : arith_exp,
    '/'       : arith_exp,
    '=='      : rel_exp,
    '<='      : rel_exp,
    '<'       : rel_exp,
    '>'       : rel_exp,
    '>='      : rel_exp,
    '!='      : rel_exp
}


label_id = 0

# function to generate labels

def label():
    global label_id
    s =  'L' + str(label_id)
    label_id += 1
    return s


