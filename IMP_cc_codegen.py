from IMP_state import state
from grammar_stuff import assert_match

# codegen: this is the code generator for the IMP compiler

# The generated code is a list of JVM bytecode instructions for the corresponding statements in IMP

i = 0
j = 0
    
#########################################################################
# node functions
def seq(node):

    global i,j 
    (SEQ, s1, s2) = node
    assert_match(SEQ, 'seq')
    
    stmt = walk(s1)
    lst = walk(s2)

    return stmt + lst

#########################################################################
def nil(node):
    
    global i,j 
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    code = [('return',)]
    i = 0
    j = 0
    return code
    
#########################################################################
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
        #code = [('store', name, exp_code)]
    #print(exp_code)
    #code = [('iconst_'+exp_code,)]
    #code += [('istore_'+exp_code,)]
    return code

#########################################################################
def get_stmt(node):

    global i
    (GET, name) = node
    assert_match(GET, 'get')
    value = input()
    state.symbol_table[name] = value
    #code = [('input', name)]
    code = [('invokevirtual',)]
    code += [('istore_'+str(i),)]
    i+=1
    
    return code

#########################################################################
def put_stmt(node):

    (PUT, exp) = node
    assert_match(PUT, 'put')
    
    exp_code = walk(exp)

    #code = [('print', exp_code)]
    code = [('invokevirtual',)]
    
    return code

#########################################################################
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
    if cond[0] == '<':
        code += [('if_icmpge\t'+false_label,)]
    elif cond[0] == '>':
        code += [('if_icmple\t'+false_label,)]
    elif cond[0] == '>=':
        code += [('if_icmplt\t'+false_label,)]
    elif cond[0] == '<=':
        code += [('if_icmpgt\t'+false_label,)]
    elif cond[0] == '==':
        code += [('if_icmpne\t'+false_label,)]
    elif cond[0] == '!=':
        code += [('if_icmpeq\t'+false_label,)]   
        
    
    code += [(true_label + ':',)]
    code += body_code
    code += [('goto\t'+begin_label,)]
    code += [(false_label + ':',)]
        
    #code += [('jumpF', cond_code, bottom_label)]
    #code += body_code
    #code += [('jump', top_label)]
    #code += [(true_label + ':',)]
    #code += [('noop',)]

    return code

#########################################################################
def if_stmt(node):

    try: # try the if-then pattern
        (IF, cond, s1, (NIL,)) = node
        assert_match(IF, 'if')
        assert_match(NIL, 'nil')
    
    except ValueError: # pattern didn't match
        # try the if-then-else pattern
        (IF, cond, s1, s2) = node
        assert_match(IF, 'if')
        
        else_label = label()
        end_label = label()
        cond_code = walk(cond)
        stmt1_code = walk(s1)
        stmt2_code = walk(s2)

        code = [('jumpF', cond_code, else_label)]
        code += stmt1_code
        code += [('jump', end_label)]
        code += [(else_label + ':',)]
        code += stmt2_code
        code += [(end_label + ':',)]
        code += [('noop',)]

        return code

    else:
        end_label = label();
        cond_code = walk(cond)
        stmt1_code = walk(s1)

        code = [('jumpF', cond_code, end_label)]
        code += stmt1_code
        code += [(end_label + ':',)]
        code += [('noop',)]

        return code

#########################################################################
def block_stmt(node):

    (BLOCK, s) = node
    assert_match(BLOCK, 'block')

    code = walk(s)
    
    return code

#########################################################################
def binop_exp(node):

    global i,j 
    (OP, c1, c2) = node
    if OP not in ['+', '-', '*', '/', '==', '<=', '<', '>', '!=', '>=']:
        raise ValueError("pattern match failed on " + OP)
    
    lcode = walk(c1)
    rcode = walk(c2)
    print(lcode,rcode,c1,c2)
    val1 = state.symbol_table.get(lcode, 0)
    val2 = state.symbol_table.get(rcode, 0)
    output = int(val1)+int(val2)  
    if OP == '+':
        code = [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('iadd',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP == '-':
        code = [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('isub',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP == '*':
        code = [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('imul',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP == '/':
        code = [('iload_'+str(j),)]
        j+=1
        code += [('iload_'+str(j),)]
        j+=1
        code += [('idiv',)]
        code += [('istore_'+str(i),)]
        i+=1
        
    if OP in ['<','>','==', '<=', '!=', '>=']:
        if c1[0] == 'id':
            code = [('iload_'+str(j),)]
            j+=1
        elif c2[0] == 'id':
            code = [('iload_'+str(j),)] 
            j+=1
        if c1[0] == 'integer':
            code += [('iconst_'+lcode,)]
        elif c2[0] == 'integer':
            code += [('iconst_'+rcode,)]
        
                 
    #code = '(' + OP + ' ' + lcode + ' ' + rcode + ')'

    return code

#########################################################################
def integer_exp(node):

    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')

    return str(value)

#########################################################################
def id_exp(node):
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    return name

#########################################################################
def uminus_exp(node):
    
    (UMINUS, e) = node
    assert_match(UMINUS, 'uminus')
    
    code = walk(e)

    return '-' + code

#########################################################################
def not_exp(node):
    
    (NOT, e) = node
    assert_match(NOT, 'not')
    
    code = walk(e)

    return '!' + code

#########################################################################
def paren_exp(node):
    
    (PAREN, exp) = node
    assert_match(PAREN, 'paren')
    
    exp_code = walk(exp)

    return exp_code

#########################################################################
# walk
#########################################################################
def walk(node):
    node_type = node[0]
    
    if node_type in dispatch_dict:
        node_function = dispatch_dict[node_type]
        return node_function(node)
    
    else:
        raise ValueError("walk: unknown tree node type: " + node_type)

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
    'id'      : id_exp,
    'uminus'  : uminus_exp,
    'not'     : not_exp,
    'paren'   : paren_exp,
    '+'       : binop_exp,
    '-'       : binop_exp,
    '*'       : binop_exp,
    '/'       : binop_exp,
    '=='      : binop_exp,
    '<='      : binop_exp,
    '<'       : binop_exp

}

#########################################################################
label_id = 0

def label():
    global label_id
    s =  'L' + str(label_id)
    label_id += 1
    return s


