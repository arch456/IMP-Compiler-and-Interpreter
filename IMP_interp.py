#!/usr/bin/env python
# Interpreter for IMP language

from argparse import ArgumentParser
from IMP_lex import lexer
from IMP_frontend_gram import parser
from IMP_state import state
from IMP_interp_walk import walk

def interp(input_stream):

    # initialize the state object
    state.initialize()

    # build the AST
    parser.parse(input_stream, lexer=lexer)

    # walk the AST
    walk(state.AST)

if __name__ == "__main__":
    # parse command line arguments
    aparser = ArgumentParser()
    aparser.add_argument('input')

    args = vars(aparser.parse_args())

    f = open(args['input'], 'r')
    input_stream = f.read()
    f.close()

    # execute the interpreter
    interp(input_stream=input_stream)