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

line = -1
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

def print_usage():
    print ("Usage: %s [OPTIONS] {-i|--input} <inputfile>" %__file__)
    print ("Available options:")
    print ("           -h, --help               Display usage infprmation")
    sys.exit()


def open_required_files(inputFile, intermFile, cequivFile, outputFile):
    global inFile, intFile, ceqFile, outFile

    try:
        inFile = open(inputFile, 'r', encoding='utf-8')
        intFile = open(intermFile, 'w', encoding='utf-8')
        cequivFile = open(cequivFile, 'w', encoding='utf-8')
        outputFile = open(outputFile, 'w', encoding='utf-8')
    except OSError as oserr:
        print(err)

# Lexical Analyzer
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
                print('Comment in line ', comment_start_pos, ' never closed!')
                sys.exit()
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

    intermFile = inputFile[:-3] + ".int"
    cequivFile = inputFile[:-3] + ".c"
    outputFile = inputFile[:-3] + ".asm"

    open_required_files(inputFile, intermFile, cequivFile, outputFile)

    for i in range(0, 50):
        print(lex())


if __name__ == "__main__":
    main(sys.argv[1:])
