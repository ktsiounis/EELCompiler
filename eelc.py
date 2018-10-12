import sys, getopt, os
from enum import Enum

class TokenType(Enum):
    IDENT       = 0
    NUMBER      = 1
    # Brackets
    LPAREN      = 2
    RPAREN      = 3
    LBRACE      = 4
    RBRACE      = 5
    LBRACKET    = 6
    RBRACKET    = 7
    # Other punctuation marks
    COMMA       = 8
    COLON       = 9
    SEMICOLON   = 10
    # Relational Operators
    LSS         = 11
    GTR         = 12
    LEQ         = 13
    GEQ         = 14
    EQL         = 15
    NEQ         = 16
    # Assignment
    BECOMES     = 17
    # Arithmetic Operators
    PLUS        = 18
    MINUS       = 19
    TIMES       = 20
    SLASH       = 21
    # Keywords
    ANDSYM      = 22
    NOTSYM      = 23
    ORSYM       = 24
    DECLARESYM  = 25
    ENDDECLSYM  = 26
    REPEATSYM   = 27
    IFSYM       = 28
    ELSESYM     = 29
    EXITSYM     = 30
    PROCSYM     = 31
    FUNCSYM     = 32
    PRINTSYM    = 33
    CALLSYM     = 34
    INSYM       = 35
    INOUTSYM    = 36
    SELECTSYM   = 37
    PROGRAMSYM  = 38
    RETURNSYM   = 39
    WHILESYM    = 40
    ENDWHILESYM = 41
    ENDPROGMSYM = 42
    ENDREPSYM   = 43
    THENSYM     = 44
    ENDIFSYM    = 45
    ENDPROCSYM  = 46
    ENDFUNKSYM  = 47
    INPUTSYM    = 48
    SWITCHSYM   = 49
    CASESYM     = 50
    ENDSTHSYM   = 51
    FORSYM      = 52
    WHENSYM     = 53
    ENDFORSYM   = 54
    TRUESYM     = 55
    FALSESYM    = 56
    # EOF
    EOF         = 57

tokens       = {
    '(':           TokenType.LPAREN,
    ')':           TokenType.RPAREN,
    '{':           TokenType.LBRACE,
    '}':           TokenType.RBRACE,
    '[':           TokenType.LBRACKET,
    ']':           TokenType.RBRACKET,
    ',':           TokenType.COMMA,
    ':':           TokenType.COLON,
    ';':           TokenType.SEMICOLON,
    '<':           TokenType.LSS,
    '>':           TokenType.GTR,
    '<=':          TokenType.LEQ,
    '>=':          TokenType.GEQ,
    '=':           TokenType.EQL,
    '<>':          TokenType.NEQ,
    ':=':          TokenType.BECOMES,
    '+':           TokenType.PLUS,
    '-':           TokenType.MINUS,
    '*':           TokenType.TIMES,
    '/':           TokenType.SLASH,
    'and':         TokenType.ANDSYM,
    'not':         TokenType.NOTSYM,
    'or':          TokenType.ORSYM,
    'declare':     TokenType.DECLARESYM,
    'enddeclare':  TokenType.ENDDECLSYM,
    'repeat':      TokenType.REPEATSYM,
    'endrepeat':   TokenType.ENDREPSYM,
    'exit':        TokenType.EXITSYM,
    'if':          TokenType.IFSYM,
    'then':        TokenType.THENSYM,
    'else':        TokenType.ELSESYM,
    'endif':       TokenType.ENDIFSYM,
    'switch':      TokenType.SWITCHSYM,
    'case':        TokenType.CASESYM,
    'endswitch':   TokenType.ENDSTHSYM,
    'forcase':     TokenType.FORSYM,
    'when':        TokenType.WHENSYM,
    'endforcase':  TokenType.ENDFORSYM,
    'procedure':   TokenType.PROCSYM,
    'endprocedure':TokenType.ENDPROCSYM,
    'function':    TokenType.FUNCSYM,
    'endfunction': TokenType.ENDFUNKSYM,
    'print':       TokenType.PRINTSYM,
    'input':       TokenType.INPUTSYM,
    'call':        TokenType.CALLSYM,
    'in':          TokenType.INSYM,
    'inout':       TokenType.INOUTSYM,
    'select':      TokenType.SELECTSYM,
    'program':     TokenType.PROGRAMSYM,
    'endprogram':  TokenType.ENDPROGMSYM,
    'return':      TokenType.RETURNSYM,
    'while':       TokenType.WHILESYM,
    'endwhile':    TokenType.ENDWHILESYM,
    'true':        TokenType.TRUESYM,
    'false':       TokenType.FALSESYM,
    'EOF':         TokenType.EOF}

class Token():
    def __init__(self, tktype, tkval, tkl):
        self.tktype, self.tkval, self.tkl = tktype, tkval, tkl

    def __str__(self):
        return  '(' + str(self.tktype)+ ', \'' + str(self.tkval) \
            + '\', ' + str(self.tkl) + ')'

class Quad():
    def __init__(self, label, op, arg1, arg2, res):
        self.label, self.op, self.arg1, self.arg2 = label, op, arg1, arg2
        self.res = res

    def __str__(self):
        return '(' + str(self.label) + ': ' + str(self.op)+ ', ' + \
            str(self.arg1) + ', ' + str(self.arg2) + ', ' + str(self.res) + ')'

    def tofile(self):
        return str(self.label) + ': (' + str(self.op)+ ', ' + \
            str(self.arg1) + ', ' + str(self.arg2) + ', ' + str(self.res) + ')'

#################################
#                               #
#       Global Variables        #
#                               #
#################################
line = 0
token = Token(None, None, None)
programName = ''
quadcode = list()
nextlabel = 0
nextTemp = 1
tempvars = dict()

#################################
#                               #
#       General Functions       #
#                               #
#################################
def print_usage():
    print ("Usage: %s [OPTIONS] {-i|--input} <inputfile>" %__file__)
    print ("Available options:")
    print ("           -h, --help               Display usage infprmation")
    sys.exit()

def print_error_and_exit(errorType, line, msg):
    print('%s: File %s, line %d:' % (errorType, inFile.name, line), ' ', msg)
    close_required_files()
    if errorType == "Syntax Error":
        os.remove(intFile.name)
        os.remove(ceqFile.name)
        os.remove(outFile.name)
    sys.exit()

def open_required_files(inputFile, intermFile, cequivFile, outputFile):
    global inFile, intFile, ceqFile, outFile

    try:
        inFile = open(inputFile, 'r', encoding='utf-8')
        intFile = open(intermFile, 'w', encoding='utf-8')
        ceqFile = open(cequivFile, 'w', encoding='utf-8')
        outFile = open(outputFile, 'w', encoding='utf-8')
    except OSError as oserr:
        print(oserr)

def close_required_files():
    global inFile
    inFile.close()
    intFile.close()
    ceqFile.close()
    outFile.close()

#################################
#                               #
#       Lexical Analyzer        #
#                               #
#################################
def lex():
    global line

    buffer = []
    state = 0
    DONE = -2
    tkn_start_pos = tkn_end_pos = -1
    comment_start_pos = comment_end_pos = -1
    unget = False

    while state != DONE:
        c = inFile.read(1)
        buffer.append(c)
        if state == 0:
            if c.isalpha():
                state = 1
            elif c.isdigit():
                state = 2
            elif c.isspace():
                state = 0
            elif c == '<':
                state = 3
            elif c == '>':
                state = 4
            elif c == ':':
                state = 5
            elif c == '/':
                state = 6
            elif c == '':
                state = DONE
                return Token(TokenType.EOF, 'EOF', line)
            elif c in ('+', '-', '*', '=', ',', ';', '{', '}', '(', ')', '[', ']'):
                state = DONE
            else:
                print ("Error in lexical analysis!")
        elif state == 1:
            if not c.isalnum():
                unget = True
                state = DONE
        elif state == 2:
            if not c.isdigit():
                if c.isalpha():
                    print("Variables should begin with alphabetic character")
                unget = True
                state = DONE
        elif state == 3:
            if c != '=' and c != '>':
                unget = True
            state = DONE
        elif state == 4:
            if c != '=':
                unget = True
            state = DONE
        elif state == 5:
            if c != '=':
                unget = True
            state = DONE
        elif state == 6:
            if c == '*': #Comment start
                state = 7
                comment_start_pos = line
            elif c == '/': #Comment start
                state = 9
            else: #Just a slash
                unget = True
                state = DONE
        elif state == 7:
            if c == '': # EOF
                print_error_and_exit(line, 'Comment in line %d never closed' %comment_start_pos)
            elif c == '*':
                state = 8
        elif state == 8:
            if c == '/': #Comment close
                del buffer[:]
                state = 0
            else:
                state = 7
        elif state == 9:
            if c == '\n':
                del buffer[:-1]
                state = 0

        if c.isspace():
            del buffer[-1]
            unget = False
            if c == '\n':
                line += 1

    if unget == True:
        del buffer[-1]
        if c != '': #if not EOF
            inFile.seek(inFile.tell() - 1)

    buffer_cont = ''.join(buffer)
    if buffer_cont not in tokens.keys():
        if buffer_cont.isdigit():
            tok = Token(TokenType.NUMBER, buffer_cont, line)
        else:
            tok = Token(TokenType.IDENT, buffer_cont, line)
    else:
        tok = Token(tokens[buffer_cont], buffer_cont, line)

    del buffer[:]

    return tok

#################################
#                               #
#        Syntax Analyzer        #
#                               #
#################################
def parser():
    global token
    token = lex()
    program()
    generate_int_code()

def program():
    global token, programName
    if token.tktype == TokenType.PROGRAMSYM:
        token = lex()
        if token.tktype == TokenType.IDENT:
            programName = token.tkval
            token = lex()
            block(programName)
            if token.tktype != TokenType.ENDPROGMSYM:
                print_error_and_exit("Syntax Error", line, "Keyword 'endprogram' was expected but found %s instead" %token.tkval)
        else:
            print_error_and_exit("Syntax Error", line, "Program name was expected but found %s instead" %token.tkval)
    else:
        print_error_and_exit("Syntax Error", line, "Keyword 'program' was expected but found %s instead" %token.tkval)

def block(name):
    declarations()
    subprograms()
    genquad('begin_block', name)
    statements()
    if name == programName:
        halt_label = nextquad()
        genquad('halt')
    genquad('end_block', name)

def declarations():
    global token
    if token.tktype == TokenType.DECLARESYM:
        token = lex()
        varlist()
        if token.tktype != TokenType.ENDDECLSYM:
            print_error_and_exit("Syntax Error", line, "Keyword 'enddeclare' was expected but found %s instead" %token.tkval)
        token = lex()

def varlist():
    global token
    if token.tktype == TokenType.IDENT:
        token = lex()
        while token.tktype == TokenType.COMMA:
            token = lex()
            if token.tktype != TokenType.IDENT:
                print_error_and_exit("Syntax Error", line, "Expected variable declaration but found %s instead" %token.tkval)
            token = lex()

def subprograms():
    global token
    while token.tktype == TokenType.PROCSYM or token.tktype == TokenType.FUNCSYM:
        procorfunc()

def procorfunc():
    global token
    if token.tktype == TokenType.PROCSYM:
        token = lex()
        if token.tktype != TokenType.IDENT:
            print_error_and_exit("Syntax Error", line, "Procedure name expected but found %s instead" %token.tkval)
        name = token.tkval
        token = lex()
        procorfuncbody(name)
        if token.tktype != TokenType.ENDPROCSYM:
            print_error_and_exit("Syntax Error", line, "Keyword 'endprocedure' was expected but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.FUNCSYM:
        token = lex()
        if token.tktype != TokenType.IDENT:
            print_error_and_exit("Syntax Error", line, "Function name expected but found %s instead" %token.tkval)
        name = token.tkval
        token = lex()
        procorfuncbody(name)
        if token.tktype != TokenType.ENDFUNKSYM:
            print_error_and_exit("Syntax Error", line, "Keyword 'endfunction' was expected but found %s instead" %token.tkval)
        token = lex()

def procorfuncbody(name):
    formalpars()
    block(name)

def formalpars():
    global token
    if token.tktype != TokenType.LPAREN:
        print_error_and_exit("Syntax Error", line, "Character '(' was expected but found %s instead" %token.tkval)
    token = lex()
    formalparlist()
    if token.tktype != TokenType.RPAREN:
        print_error_and_exit("Syntax Error", line, "Character ')' was expected but found %s instead" %token.tkval)
    token = lex()

def formalparlist():
    global token
    if token.tktype == TokenType.INSYM or token.tktype == TokenType.INOUTSYM:
        token = lex()
        if token.tktype == TokenType.IDENT:
            token = lex()
            while token.tktype == TokenType.COMMA:
                token = lex()
                if token.tktype != TokenType.INSYM and token.tktype != TokenType.INOUTSYM:
                    print_error_and_exit("Syntax Error", line, "Expected keyword 'in' or 'inout' for variable declaration but found %s instead" %token.tkval)
                token = lex()
                if token.tktype != TokenType.IDENT:
                    print_error_and_exit("Syntax Error", line, "Expected variable declaration but found %s instead" %token.tkval)
                token = lex()
        else:
            print_error_and_exit("Syntax Error", line, "Expected variable declaration but found %s instead" %token.tkval)

def statements():
    global token
    statement()
    while token.tktype == TokenType.SEMICOLON:
        token = lex()
        statement()

def statement():
    global token
    if token.tktype == TokenType.IDENT:
        lhand = token.tkval
        token = lex()
        if token.tktype != TokenType.BECOMES:
            print_error_and_exit("Syntax Error", line, "Expected ':=' but found %s instead" %token.tkval)
        token = lex()
        rhand = expression()
        genquad(':=', rhand, '_', lhand)
    elif token.tktype == TokenType.IFSYM:
        token = lex()
        condition()
        if token.tktype != TokenType.THENSYM:
            print_error_and_exit("Syntax Error", line, "Expected 'then' but found %s instead" %token.tkval)
        token = lex()
        statements()
        elsepart()
        if token.tktype != TokenType.ENDIFSYM:
            print_error_and_exit("Syntax Error", line, "Expected 'endif' but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.WHILESYM:
        token = lex()
        condition()
        statements()
        if token.tktype != TokenType.ENDWHILESYM:
            print_error_and_exit("Syntax Error", line, "Expected 'endwhile' but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.REPEATSYM:
        token = lex()
        statements()
        if token.tktype != TokenType.ENDREPSYM:
            print_error_and_exit("Syntax Error", line, "Expected 'endrepeat' but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.EXITSYM:
        token = lex()
    elif token.tktype == TokenType.SWITCHSYM:
        switchStartPos = line
        token = lex()
        expression()
        while token.tktype != TokenType.ENDSTHSYM:
            if token.tktype != TokenType.CASESYM:
                print_error_and_exit("Syntax Error", line, "Expected 'case' but found %s instead" %token.tkval)
            token = lex()
            expression()
            if token.tktype != TokenType.COLON:
                print_error_and_exit("Syntax Error", line, "Expected ':' but found %s instead" %token.tkval)
            token = lex()
            statements()
            if token.tktype == TokenType.EOF:
                print_error_and_exit("Syntax Error", switchStartPos, "Switch statement never closed")
        token = lex()
    elif token.tktype == TokenType.FORSYM:
        forStartPos = line
        token = lex()
        while token.tktype != TokenType.ENDFORSYM:
            if token.tktype != TokenType.WHENSYM:
                print_error_and_exit("Syntax Error", line, "Expected 'when' but found %s instead" %token.tkval)
            token = lex()
            condition()
            if token.tktype != TokenType.COLON:
                print_error_and_exit("Syntax Error", line, "Expected ':' but found %s instead" %token.tkval)
            token = lex()
            statements()
            if token.tktype == TokenType.EOF:
                print_error_and_exit("Syntax Error", forStartPos, "Forcase statement never closed")
        token = lex()
    elif token.tktype == TokenType.CALLSYM:
        token = lex()
        id = token.tkval
        if token.tktype != TokenType.IDENT:
            print_error_and_exit("Syntax Error", line, "Expected function or procedure id but found %s instead" %token.tkval)
        token = lex()
        actualpars()
        genquad('call', id)
    elif token.tktype == TokenType.RETURNSYM:
        token = lex()
        exp = expression()
        genquad('retv', exp)
    elif token.tktype == TokenType.PRINTSYM:
        token = lex()
        exp = expression()
        genquad('out', exp)
    elif token.tktype == TokenType.INPUTSYM:
        token = lex()
        exp = expression()
        genquad('inp', exp)

def actualpars():
    global token
    if token.tktype != TokenType.LPAREN:
        print_error_and_exit("Syntax Error", line, "Expected '(' but found %s instead" %token.tkval)
    token = lex()
    actualparlist()
    if token.tktype != TokenType.RPAREN:
        print_error_and_exit("Syntax Error", line, "Expected ')' but found %s instead" %token.tkval)
    token = lex()
    return True

def actualparlist():
    global token
    if token.tktype != TokenType.RPAREN:
        actualparlistitem()
        while token.tktype == TokenType.COMMA:
            token = lex()
            actualparlistitem()

def actualparlistitem():
    global token
    if token.tktype != TokenType.INSYM and token.tktype != TokenType.INOUTSYM:
        print_error_and_exit("Syntax Error", line, "Expected 'in' or 'inout' but found %s instead" %token.tkval)
    elif token.tktype == TokenType.INSYM:
        token = lex()
        exp = expression()
        genquad('par', exp, 'CV')
    elif token.tktype == TokenType.INOUTSYM:
        token = lex()
        par = token.tkval
        if token.tktype != TokenType.IDENT :
            print_error_and_exit("Syntax Error", line, "Expected variable identifier but found %s instead" %token.tkval)
        token = lex()
        genquad('par', par, 'REF')

def expression():
    global token
    if token.tktype in (TokenType.PLUS, TokenType.MINUS):
        token = lex()
    term1 = term()
    while token.tktype == TokenType.PLUS or token.tktype == TokenType.MINUS:
        op = token.tkval
        token = lex()
        term2 = term()
        tmpvar = newtemp()
        genquad(op, term1, term2, tmpvar)
        term1 = tmpvar
    return term1

def term():
    global token
    factor1 = factor()
    while token.tktype == TokenType.TIMES or token.tktype == TokenType.SLASH:
        op = token.tkval
        token = lex()
        factor2 = factor()
        tmpvar = newtemp()
        genquad(op, factor1, factor2, tmpvar)
        factor1 = tmpvar
    return factor1

def factor():
    global token
    if token.tktype == TokenType.RPAREN:
        token = lex()
        retval = expression()
        if token.tktype == TokenType.RPAREN:
            print_error_and_exit("Syntax Error", line, "Expected ')' but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.IDENT:
        retval = token.tkval
        token = lex()
        tail = idtail()
        if tail != None:
            funcret = newtemp()
            genquad('par', funcret, 'RET')
            genquad('call', retval)
            retval = funcret
    else:
        retval = token.tkval
        token = lex()
    return retval

def idtail():
    global token
    if token.tktype == TokenType.LPAREN:
        return actualpars()

def condition():
    global token
    boolterm()
    while token.tktype == TokenType.ORSYM:
        token = lex()
        boolterm()

def boolterm():
    global token
    boolfactor()
    while token.tktype == TokenType.ANDSYM:
        token = lex()
        boolterm()

def boolfactor():
    global token
    if token.tktype == TokenType.NOTSYM:
        token = lex()
        if token.tktype != TokenType.LBRACKET:
            print_error_and_exit("Syntax Error", line, "Expected '[' but found %s instead" %token.tkval)
        token = lex()
        condition()
        if token.tktype != TokenType.RBRACKET:
            print_error_and_exit("Syntax Error", line, "Expected ']' but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.LBRACKET:
        token = lex()
        condition()
        if token.tktype != TokenType.RBRACKET:
            print_error_and_exit("Syntax Error", line, "Expected ']' but found %s instead" %token.tkval)
        token = lex()
    elif token.tktype == TokenType.TRUESYM:
        token = lex()
    elif token.tktype == TokenType.FALSESYM:
        token = lex()
    else:
        expression()
        if not token.tktype in (TokenType.EQL, TokenType.LSS,
                                TokenType.NEQ, TokenType.LEQ,
                                TokenType.GEQ, TokenType.GTR):
            print_error_and_exit("Syntax Error", line, "Expected relational operator but found %s instead" %token.tkval)
        token = lex()
        expression()

def elsepart():
    global token
    if token.tktype == TokenType.ELSESYM:
        token = lex()
        statements()


#################################
#                               #
#      Intermediate Code        #
#         Generation            #
#                               #
#################################
def nextquad():
    return nextlabel

def genquad(op=None, x='_', y='_', z='_'):
    global nextlabel
    label = nextlabel
    nextlabel += 1
    newquad = Quad(label, op, x, y, z)
    quadcode.append(newquad)

def newtemp():
    global tmpvars, nextTemp
    temp = 'T_'+str(nextTemp)
    tempvars[temp] = None
    nextTemp += 1
    return temp

def emptylist():
    return list()

def makelist(label):
    newlist = list()
    newlist.append(label)
    return newlist

def merge(list1, list2):
    return list1 + list2

def backpatch(list, z):
    global quadcode
    for quad in quadcode:
        if quad.label in list:
            quad.res = z

def generate_int_code():
    for quad in quadcode:
        intFile.write(quad.tofile() + '\n')
    intFile.close()



def main(argv):
    inputFile = ''
    intermFile = ''
    cequivFile = ''
    outputFile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "ifile="])
    except getopt.GetoptError as err:
        print (err)
        print_usage()

    if not opts:
        print_usage()

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print_usage()
        elif opt in ("-i", "--ifile"):
            inputFile = arg

    if inputFile == '':
        print ("Option {-i|--input} is required")
        print_usage()
    elif inputFile[-3:] != ".ci":
        print ("Invalid file type")
        sys.exit()

    intermFile = inputFile[:-3] + ".int"
    cequivFile = inputFile[:-3] + ".c"
    outputFile = inputFile[:-3] + ".asm"

    open_required_files(inputFile, intermFile, cequivFile, outputFile)

    parser()


if __name__ == "__main__":
    main(sys.argv[1:])
