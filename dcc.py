import sys, getopt, os
from enum import Enum

class TokenType(Enum):
    IDENT      = 0
    NUMBER     = 1
    # Brackets
    LPAREN     = 2
    RPAREN     = 3
    LBRACE     = 4
    RBRACE     = 5
    LBRACKET   = 6
    RBRACKET   = 7
    # Other punctuation marks
    COMMA      = 8
    COLON      = 9
    SEMICOLON  = 10
    # Relational Operators
    LSS        = 11
    GTR        = 12
    LEQ        = 13
    GEQ        = 14
    EQL        = 15
    NEQ        = 16
    # Assignment
    BECOMES    = 17
    # Arithmetic Operators
    PLUS       = 18
    MINUS      = 19
    TIMES      = 20
    SLASH      = 21
    # Keywords
    ANDSYM     = 22
    NOTSYM     = 23
    ORSYM      = 24
    DECLARESYM = 25
    ENDDECLSYM = 26
    DOSYM      = 27
    IFSYM      = 28
    ELSESYM    = 29
    EXITSYM    = 30
    PROCSYM    = 31
    FUNCSYM    = 32
    PRINTSYM   = 33
    CALLSYM    = 34
    INSYM      = 35
    INOUTSYM   = 36
    SELECTSYM  = 37
    PROGRAMSYM = 38
    RETURNSYM  = 39
    WHILESYM   = 40
    DEFAULTSYM = 41
    # EOF
    EOF        = 42

tokens       = {
    '(':          TokenType.LPAREN,
    ')':          TokenType.RPAREN,
    '{':          TokenType.LBRACE,
    '}':          TokenType.RBRACE,
    '[':          TokenType.LBRACKET,
    ']':          TokenType.RBRACKET,
    ',':          TokenType.COMMA,
    ':':          TokenType.COLON,
    ';':          TokenType.SEMICOLON,
    '<':          TokenType.LSS,
    '>':          TokenType.GTR,
    '<=':         TokenType.LEQ,
    '>=':         TokenType.GEQ,
    '=':          TokenType.EQL,
    '<>':         TokenType.NEQ,
    ':=':         TokenType.BECOMES,
    '+':          TokenType.PLUS,
    '-':          TokenType.MINUS,
    '*':          TokenType.TIMES,
    '/':          TokenType.SLASH,
    'and':        TokenType.ANDSYM,
    'not':        TokenType.NOTSYM,
    'or':         TokenType.ORSYM,
    'declare':    TokenType.DECLARESYM,
    'enddeclare': TokenType.ENDDECLSYM,
    'do':         TokenType.DOSYM,
    'if':         TokenType.IFSYM,
    'else':       TokenType.ELSESYM,
    'exit':       TokenType.EXITSYM,
    'procedure':  TokenType.PROCSYM,
    'function':   TokenType.FUNCSYM,
    'print':      TokenType.PRINTSYM,
    'call':       TokenType.CALLSYM,
    'in':         TokenType.INSYM,
    'inout':      TokenType.INOUTSYM,
    'select':     TokenType.SELECTSYM,
    'program':    TokenType.PROGRAMSYM,
    'return':     TokenType.RETURNSYM,
    'while':      TokenType.WHILESYM,
    'default':    TokenType.DEFAULTSYM,
    'EOF':        TokenType.EOF}

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


def lex():

    state = 0
    DONE = -1


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


if __name__ == "__main__":
    main(sys.argv[1:])
