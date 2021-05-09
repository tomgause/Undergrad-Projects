import re
import sys

inputString = ""
nextToken = ""
tabs = ""

def lex():
    global inputString
    global nextToken
    global tabs

    print(tabs, "LEX: inputString => ", inputString)
    print(tabs, "LEX: nextToken => ", nextToken)
    print(tabs, "LEX: lexing...")

    termList = ['program', 'if', 'while', 'begin', 'read', 'write', 'then', 'endprogram', \
                'def', 'return', 'for', 'print', 'end', 'do', 'else', 'call']
    symList = ['(', ')' , ',' , ';']
    relOps = ['=', '<>', '<', '<=', '>=', '>']

    # (  )  ,  ;
    p = re.compile(' *([\(\),;]) *')
    m = p.match(inputString)
    if (m != None):
        if (m.group(1) in symList):
            nextToken = m.group(1)
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    # :=
    p = re.compile('(:=) ')
    m = p.match(inputString)
    if (m != None):
        nextToken = ':='
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return

    # adding_operator | sign
    p = re.compile('([+-]) ')
    m = p.match(inputString)
    if (m != None):
        if (nextToken == ')' or nextToken == '<variable>' or nextToken == '<constant>'):
            nextToken = '<adding_operator>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return
        else:
            nextToken = '<sign>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    #multiplying_operator
    p = re.compile('([\*\/%]) ')
    m = p.match(inputString)
    if (m != None):
        nextToken = '<multiplying_operator>'
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return

    #relational_operator
    p = re.compile('([=><][=>]?) ')
    m = p.match(inputString)
    if (m != None):
        if (m.group(1) in relOps):
            nextToken = '<relational_operator>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    #string
    p = re.compile('(#[A-Za-z]*\w*) ')
    m = p.match(inputString)
    if (m != None):
        nextToken = '<string>'
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return

    #progname | variable
    p = re.compile('([A-Za-z]\w*) ')
    m = p.match(inputString)
    if (m != None):
        p2 = re.compile('([A-Z]\w*) ')
        m2 = p2.match(inputString)
        if (m.group(1) in termList):
            nextToken = m.group(1)
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return
        elif (m2 != None and nextToken == 'program'):
            nextToken = '<progname>'
            inputString = inputString.replace(m2.group(1) + " ", "", 1)
            return
        elif (nextToken == 'def' or nextToken == 'call'):
            nextToken = '<funcname>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return
        else:
            nextToken = '<variable>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    #constant
    p = re.compile('([0-9]\d*) ')
    m = p.match(inputString)
    if ((m != None) or ((m != None) and (inputString[0] == '0'))):
        nextToken = '<constant>'
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return

    print("Unknown symbol encountered")
    print("inputString: " + nextToken + " " + inputString )
    sys.exit(1)



def program():
    global inputString
    global nextToken
    global tabs
    print(tabs, "program hit")
    tabs += "|   "
    lex()
    if (nextToken == 'program'):
        lex()
        if (nextToken == '<progname>'):
            lex()
            compound_stmt()
        else:
            print("Expected a program name; got " + nextToken)
            sys.exit(3)
    else:
        print("Expected 'program'; got " + nextToken)
        sys.exit(2)

    print(tabs, "exiting program...")
    tabs = tabs.replace("|   ", "", 1)

def compound_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "compound_stmt hit")
    tabs += "|   "
    if (nextToken == '('):
        lex()
        stmt()
        while (nextToken == ';'):
            lex()
            stmt()
        if (nextToken == ')'):
            lex()
            if (nextToken == 'endprogram'):
                print(tabs, "exiting compound_stmt then program...")
                tabs = tabs.replace("|   ", "", 1)
                return
            print(tabs, "exiting compound_stmt...")
            tabs = tabs.replace("|   ", "", 1)
            return
        else:
            print("Error: expected ), got ", nextToken)
            sys.exit(4)
    else:
        print("Error: expected (, got ", nextToken)
        sys.exit(42)

    print(tabs, "exiting compound_stmt...")
    tabs = tabs.replace("|   ", "", 1)

def stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "stmt hit")
    tabs += "|   "
    if (nextToken == 'read' or nextToken == 'write' or nextToken == 'print' or \
        nextToken == '<variable>' or nextToken == 'def'):
        simple_stmt()
    elif (nextToken == 'if' or nextToken == 'while' or \
          nextToken == '(' or nextToken == 'for'):
        structured_stmt()
    else:
        print("Error: Expected statement start, got ", nextToken)
        sys.exit(6)

    print(tabs, "exiting stmt...")
    tabs = tabs.replace("|   ", "", 1)

def simple_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "simple_stmt hit")
    tabs += "|   "
    if (nextToken == '<variable>'):
        assignment_stmt()
    elif (nextToken == 'read'):
        read_stmt()
    elif (nextToken == 'write'):
        write_stmt()
    elif (nextToken == 'def'):
        function_stmt()
    elif (nextToken == 'print'):
        print_stmt()
    else:
        print("Error: Expected read, write, or assignment, got ", nextToken)
        sys.exit(0)

    print(tabs, "exiting simple_stmt...")
    tabs = tabs.replace("|   ", "", 1)

def read_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "read_stmt hit")
    tabs += "|   "
    lex()
    if (nextToken == '('):
        lex()
        if (nextToken == '<variable>'):
            lex()
            while (nextToken == ','):
                lex()
                if (nextToken == '<variable>'):
                    lex()
                else:
                    print("Error in read: Expected <variable> following ',', got ", nextToken)
                    sys.exit(0)
            if (nextToken == ')'):
                lex()
                print(tabs, "exiting read_stmt...")
                tabs = tabs.replace("|   ", "", 1)
                return
            else:
                print("Error: expected ), got ", nextToken)
                sys.exit(0)
            lex()
        else:
            print("Error in read: Expected <variable> following read(, got ", nextToken)
            sys.exit(0)
    else:
        print("Error in read: Expected ( following read, got ", nextToken)
        sys.exit(0)

def write_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "write_stmt hit")
    tabs += "|   "
    lex()
    if (nextToken == '('):
        lex()
        expression()
        while (nextToken == ','):
            lex()
            expression()
        if (nextToken == ')'):
            lex()
            print(tabs, "exiting write_stmt...")
            tabs = tabs.replace("|   ", "", 1)
            return
        else:
            print("Error in write: expected ), got ", nextToken)
            sys.exit(0)
    else:
        print("Error in write: Expected ( following write, got ", nextToken)
        sys.exit(0)

def function_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "function_stmt hit")
    tabs += "|   "
    lex()
    if (nextToken == '<funcname>'):
        lex()
        if (nextToken == '('):
            lex()
            if (nextToken == '<variable>'):
                lex()
                while (nextToken == ','):
                    lex()
                    if (nextToken == '<variable>'):
                        lex()
                    else:
                        print("Error in function: Expected <variable> following ',' got ", nextToken)
                        sys.exit(0)
                if (nextToken == ')'):
                    lex()
                    compound_function_stmt()
        else:
            print("Error in function: Expected ( following  <funcname>, got ", nextToken)
            sys.exit(0)
    else:
        print("Error in function: Expected <funcname> following def, got ", nextToken)
        sys.exit(0)

    print(tabs, "exiting function...")
    tabs = tabs.replace("|   ", "", 1)

def compound_function_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "compound_function_stmt hit")
    tabs += "|   "
    if (nextToken == '('):
        lex()
        stmt()
        while (nextToken == ';'):
            lex()
            stmt()
        if (nextToken == 'return'):
            lex()
            if (nextToken == ')'):
                lex()
                print(tabs, "exiting compound_function_stmt...")
                tabs = tabs.replace("|   ", "", 1)
                return
            else:
                expression()
                if (nextToken == ')'):
                    lex()
                    print(tabs, "exiting compound_function_stmt...")
                    tabs = tabs.replace("|   ", "", 1)
                    return
                else:
                    print("Error in compound_function: Expected ), got ", nextToken)
                    sys.exit(0)
        else:
            print("Error in compound_function: Expected return, got ", nextToken)
            sys.exit(0)
    else:
        print("Error in compound_function: Expected (, got ", nextToken)
        sys.exit(0)

def print_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "print_stmt hit")
    tabs += "|   "
    lex()
    if (nextToken == '('):
        lex()
        expression()
        if (nextToken == ')'):
            lex()
            print(tabs, "exiting print_stmt...")
            tabs = tabs.replace("|   ", "", 1)
            return
        else:
            print("Error in print: Expected ) after <factor>, got ", nextToken)
            sys.exit(0)
    else:
        print("Error in print: Expected (, got ", nextToken)
        sys.exit(0)

def structured_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "structured_stmt hit")
    tabs += "|   "
    if (nextToken == '('):
        compound_stmt()
    elif (nextToken == 'if'):
        if_stmt()
    elif (nextToken == 'while'):
        while_stmt()
    elif (nextToken == 'for'):
        for_stmt()
    else:
        print("Error in struct: Expected compound, if, or while, got ", nextToken)
        sys.exit(0)

    print(tabs, "exiting structured_stmt...")
    tabs = tabs.replace("|   ", "", 1)

def if_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "if_stmt hit")
    tabs += "|   "
    lex()
    expression()
    if (nextToken == 'then'):
        lex()
        stmt()
        if (nextToken == 'else'):
            lex()
            stmt()
            print(tabs, "exiting if statement...")
            tabs = tabs.replace("|   ", "", 1)
            return
        print(tabs, "exiting if statement...")
        tabs = tabs.replace("|   ", "", 1)
        return
    else:
        print("Error in if: Expected 'then', got ", nextToken)
        sys.exit(0)

def while_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "while_stmt hit")
    tabs += "|   "
    lex()
    expression()
    if (nextToken == 'do'):
        lex()
        stmt()
        print(tabs, "exiting while_stmt...")
        tabs = tabs.replace("|   ", "", 1)
        return
    else:
        print("Error in while: Expected do, got ", nextToken)
        sys.exit(0)

def for_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "for_stmt hit")
    tabs += "|   "
    lex()
    if (nextToken == '('):
        lex()
        expression()
        if (nextToken == ','):
            lex()
            expression()
            lex()
            if (nextToken == ')'):
                lex()
                if (nextToken == 'do'):
                    lex()
                    stmt()
                else:
                    print("Error in for: Expected do, got ", nextToken)
                    sys.exit(0)
            else:
                print("Error in for: Expected ), got ", nextToken)
                sys.exit(0)
        else:
            print("Error in for: Expected , following <expression>, got ", nextToken)
            sys.exit(0)
    else:
        print("Error in for: Expected (, got ", nextToken)
        sys.exit(0)

    print(tabs, "exiting for_stmt...")
    tabs = tabs.replace("|   ", "", 1)

def assignment_stmt():
    global inputString
    global nextToken
    global tabs
    print(tabs, "assignment_stmt hit")
    tabs += "|   "
    if (nextToken == '<variable>'):
        lex()
        if (nextToken == ':='):
            lex()
            expression()
        else:
            print("Error in assignment: Must assign variable with :=, instead got ", nextToken)
            sys.exit(0)
    else:
        print("Error in assignment: Expected <variable>, got ", nextToken)
        sys.exit(0)

    print(tabs, "exiting assignment_stmt...")
    tabs = tabs.replace("|   ", "", 1)

def expression():
    global inputString
    global nextToken
    global tabs
    print(tabs, "expression hit")
    tabs += "|   "
    simple_expr()
    if (nextToken == '<relational_operator>'):
        lex()
        simple_expr()

    print(tabs, "exiting expression...")
    tabs = tabs.replace("|   ", "", 1)

def simple_expr():
    global inputString
    global nextToken
    global tabs
    #print(tabs, "nextToken = ", nextToken)
    print(tabs, "simple_expr hit")
    tabs += "|   "
    if (nextToken == '<sign>'):
        lex()
    term()
    while (nextToken == '<adding_operator>'):
        lex()
        term()

    print(tabs, "exiting simple_expr...")
    tabs = tabs.replace("|   ", "", 1)

def term():
    global inputString
    global nextToken
    global tabs
    print(tabs, "term hit")
    tabs += "|   "
    factor()
    while (nextToken == '<multiplying_operator>'):
        lex()
        factor()

    print(tabs, "exiting term...")
    tabs = tabs.replace("|   ", "", 1)

def factor():
    global inputString
    global nextToken
    global tabs
    print(tabs, "factor hit")
    tabs += "|   "
    if (nextToken == '<variable>' or nextToken == '<constant>' or nextToken == '<string>'):
        lex()
    elif (nextToken == '('):
        lex()
        expression()
        if (nextToken != ')'):
            print("Error in factor: Expected ), got ", nextToken)
            sys.exit(0)
        else:
            lex()
    elif (nextToken == 'call'):
        function_call()

    else:
        print("Error in factor: Expected <variable>, <constant>, <funcname>, or (, got ", nextToken)
        sys.exit(0)

    print(tabs, "exiting factor...")
    tabs = tabs.replace("|   ", "", 1)

def function_call():
    global inputString
    global nextToken
    global tabs
    print(tabs, "function_call hit")
    tabs += "|   "
    lex()
    if (nextToken == '<funcname>'):
        lex()
        if (nextToken == '('):
            lex()
            factor()
            while (nextToken == ','):
                lex()
                factor()
            if (nextToken == ')'):
                lex()
                print(tabs, "exiting function_call...")
                tabs = tabs.replace("|   ", "", 1)
                return
            else:
                print("Error in function_call: Expected ) following <factor>, got ", nextToken)
                sys.exit(0)
        else:
            print("Error in function_call: Expected (, got ", nextToken)
            sys.exit(0)
    else:
        print("error in function_call: Expected <funcname>, got ", nextToken)
        sys.exit(0)

# loads .txt file of tests
def test(file):
    global inputString
    global nextToken
    global tabs
    f = open(file, "r")
    inputString = f.read().replace("\n", "")
    inputString = inputString.replace("\t", "")
    print("*********************************running new test...*********************************")
    print("inputString: ", inputString)
    program()
    print("The string is syntactically correct!")

# actual program
try:
    if (sys.argv[1] != None):
        test(str(sys.argv[1]))
except IndexError as e:
    inputString = input("Enter a string: ")
    program()
    print("The string is syntactically correct! :)")
