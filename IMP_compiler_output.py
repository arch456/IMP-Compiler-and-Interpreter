# The output function is used to print out the output of the IMP compiler, in a format similar to that of Java bytecode

def output(instr_stream):

    output_stream = ''
    i = 0
    
    for instr in instr_stream:

        if label_def(instr):  # label definition
            output_stream += instr[0] + '\n'

        else:          # for each instruction, put a number indicating the instruction number and a ':', like it appears in Java bytecode
            output_stream += '\t'
                
            for component in instr:
                output_stream += str(i) + ':' + ' '+ component + ' '
                i+=1           # increment the number for each instruction

            output_stream += '\n'

    return output_stream

def label_def(instr_tuple):

    instr_name = instr_tuple[0]
    
    if instr_name[-1] == ':':
        return True
    else:
        return False
    