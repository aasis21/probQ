import ply.lex as lex


# List of token names.
tokens = [
    'IDEN',
    'ALIAS',
    'COMMENT',
    'ASSIGNMENT',
    'COMMA',
    'DOT',
    'SEMICOLON',
    'COLON',
    'BAR',
    'DOUBLECOLON',
    'LEFTSQRBRACKET',
    'RIGHTSQRBRACKET',
    'LEFTSMALLBRACKET',
    'RIGHTSMALLBRACKET',
    'LEFTCURLYBRACE',
    'RIGHTCURLYBRACE',

    'NUMBER',
    'EQUAL',
    'NOTEQUAL',
    'GREATEREQUAL',
    'GREATER',
    'LESSEQUAL',
    'LESS',

    'FRACTION',
    'FLOAT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE'
]

# reserved words.
reserved = {
    'bucket':'BUCKET',
    'entity' : 'ENTITY',
    'roll' : 'ROLL',
    #'flag': 'FLAG',
    'pick' : 'PICK',
    'probab' : 'QUERY',
    #'evidence' : 'EVIDENCE',
    'equalAtmost' : 'EQUALATMOST',
    'equalAtleast' : 'EQUALATLEAST',
    'equalFew' : 'EQUALFEW',
    'equalAll' : 'EQUALALL',
    'equalAny' : 'EQUALANY',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT'
}

tokens = tokens + list(reserved.values())


# Regular expression rules for simple tokens
t_ASSIGNMENT = r'='
t_COMMA = r','
t_DOT = r'\.'
t_SEMICOLON = r';'
t_DOUBLECOLON = r'::'
t_COLON = r':'
t_BAR = r'\|'
t_LEFTSQRBRACKET = r'\['
t_RIGHTSQRBRACKET = r'\]'
t_LEFTSMALLBRACKET = r'\('
t_RIGHTSMALLBRACKET = r'\)'
t_LEFTCURLYBRACE = r'\{'
t_RIGHTCURLYBRACE = r'\}'


t_NOTEQUAL = r'!='
t_EQUAL = r'=='
t_GREATEREQUAL = r'>='
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_LESS = r'<'


t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
# A regular expression rule with some action code
# Note addition of self parameter since we're in a class

def t_FLOAT(t):
    r'(-)?(\d+\.\d+)'
    return t

def t_FRACTION(t):
    r'[1-9][0-9]*\/[1-9][0-9]*'
    t.type = 'FLOAT'
    f  = str(t.value)
    num,den = f.split( '/' )
    result = int(num)/float(den)
    t.value = str(result)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDEN(t):
    r'[a-z]([a-zA-Z_0-9áéíóúñÁÉÍÓÚÑ]*[áéíóúñÁÉÍÓÚÑa-zA-Z0-9])?'
    t.type = reserved.get(t.value,'IDEN')
    return t

def t_ALIAS(t):
    r'[A-Z]([a-zA-Z_0-9áéíóúñÁÉÍÓÚÑ]*[áéíóúñÁÉÍÓÚÑa-zA-Z0-9])?'
    t.type = reserved.get(t.value,'ALIAS')
    return t


# comment
def t_COMMENT(t):
    r'\#.*'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Test it output
def test(data):
    lex.input(data)
    while True:
         tok = lex.token()
         if not tok:
             break
         print(tok.type + ' => \' ' + str(tok.value) + ' \'')


# Build the lexer
lexer = lex.lex(debug = 0)
