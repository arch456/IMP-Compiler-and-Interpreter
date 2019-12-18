class State:
    def __init__(self):
        self.initialize()

    def initialize(self):
        # symbol table contains the values of each of the defined variables
        self.symbol_table = {}

        # this variable will contains the AST generated after parsing is done
        self.AST = None

state = State()
