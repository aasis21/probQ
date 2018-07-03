import ply.lex as lex


# List of token names.
tokens = [
    'IDEN',
    'ALIAS',
    'E_ACTION',
    'B_ACTION',
    'COMMENT',
    'ASSIGNMENT',
    'COMMA',
    'DOT',
    'SEMICOLON',
    'COLON',
    'DOUBLECOLON',
    'LEFTSQRBRACKET',
    'RIGHTSQRBRACKET',
    'LEFTSMALLBRACKET',
    'RIGHTSMALLBRACKET',
    'LEFTCURLYBRACE',
    'RIGHTCURLYBRACE',

    'NUMBER',
    'FLOAT',
    'PLUS',
    'MINUS',
]

# reserved words.
reserved = {
    'bucket':'BUCKET',
    'entity' : 'ENTITY',
    'roll' : 'ROLL',
    'flag': 'FLAG',
    'action' : 'ACTION',
    'pick' : 'PICK',
    'Probability' : 'QUERY',
    'evidence' : 'EVIDENCE',
}

tokens = tokens + list(reserved.values())


# Regular expression rules for simple tokens
t_ASSIGNMENT = r'='
t_COMMA = r','
t_DOT = r'\.'
t_SEMICOLON = r';'
t_DOUBLECOLON = r'::'
t_COLON = r':'

t_LEFTSQRBRACKET = r'\['
t_RIGHTSQRBRACKET = r'\]'
t_LEFTSMALLBRACKET = r'\('
t_RIGHTSMALLBRACKET = r'\)'
t_LEFTCURLYBRACE = r'\{'
t_RIGHTCURLYBRACE = r'\}'

# t_DIVISION = r'\/'
# t_NOTEQUAL = r'!='
# t_EQUAL = r'=='
# t_NOT = r'!'
# t_LEFTBRACE  = r'\{'
# t_RIGHTBRACE = r'\}'
# t_GREATEREQUAL = r'>='
# t_GREATER = r'>'
# t_LESSEQUAL = r'<='
# t_LESS = r'<'
# t_SUBSTRACTION = r'\-'
# t_UMINUS = r'\-'
# t_CONCAT = r'\+'
# t_MULTIPLICATION = r'\*'
# t_OR = r'(\|\|)|(OR)'
# t_MODULO = r'%'

t_PLUS = r'\+'
t_MINUS = r'\-'
# A regular expression rule with some action code
# Note addition of self parameter since we're in a class
def t_FLOAT(t):
    r'(-)?(\d+\.\d+)'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDEN(t):
    r'[a-z]([a-zA-Z_0-9áéíóúñÁÉÍÓÚÑ]*[áéíóúñÁÉÍÓÚÑa-zA-Z])?'
    t.type = reserved.get(t.value,'IDEN')
    return t

def t_ALIAS(t):
    r'[A-Z]([a-zA-Z_0-9áéíóúñÁÉÍÓÚÑ]*[áéíóúñÁÉÍÓÚÑa-zA-Z])?'
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
lex.lex(debug = 0)

source = '''
bucket pocket( coin{2},coin(0.6){1} )

X = pocket.pick(1)

Y = X.flip()

evidence( Y.equal(head) )

Probability ( equal(X, coin(0.6) )
'''

#test(source)
