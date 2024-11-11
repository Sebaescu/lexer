# PHP Lexer
import ply.lex as lex
from datetime import datetime

# Reserved words in PHP
reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "echo": "ECHO",
    "class": "CLASS",
    "function": "FUNCTION",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "array": "ARRAY",
    "print": "PRINT"
}

# List of token names
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'MOD',
    'SEMICOL',
    'VARIABLE',
    'FLOAT',
    'LBRACE',
    'RBRACE',
    'ASSIGN',
    'EQ',
    'NEQ',
    'GT',
    'LT',
    'GE',
    'LE',
    'AND_OP',
    'OR_OP',
    'NOT_OP',
    'STRING',
    'IDENTITY',
    'NIDENTITY',
    'EXPONENTIATION',
    'INCREMENT',
    'DECREMENT',
    'MACUMULATIVE',
    'Question',
    'Dot'

) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_MINUS = r'-'
t_TIMES = r'\*'
t_EXPONENTIATION = r'\*\*'
t_MACUMULATIVE = r'\*='
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MOD = r'%'
t_SEMICOL = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_EQ = r'=='
t_IDENTITY = r'==='
t_NEQ = r'!='
t_NIDENTITY = r'!=='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_NOT_OP = r'!'
t_Question = r'\?'
t_Dot = r'\.'

# Regular expression for Comments 
def t_COMMENT(t):
    r'(\/\/[^\n]*|\#[^\n]*|\/\*[\s\S]*?\*\/)'
    pass  # No return value, ignore comments

# Regular expression for FLOAT
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Regular expression for NUMBER
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Variable pattern
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# String literal (single or double quotes)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]  # Remove quotes
    return t

# Function names or reserved words
def t_FUNCTION(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, "FUNCTION")  # Check if reserved word
    return t

# Newline tracking
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def analyze_file(filename, user_git):
    with open(filename, 'r') as file:
        data = file.read()
    
    lexer.input(data)

    # Log file name
    now = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f'logs/lexer-{user_git}-{now}.txt'

    with open(log_filename, 'w') as log_file:
        log_file.write(f"Tokens y Errores para {filename}:\n\n")
        while True:
            tok = lexer.token()
            if not tok:
                break
            log_file.write(f"{tok}\n")

    print(f"Log file creado: {log_filename}")

# Run analysis
user_git = "sebaescu"  #Aqui cambian a su usuario para que quede grabado en el log
analyze_file('algoritmos/fibonacci.php', user_git)

