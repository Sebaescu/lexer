import ply.lex as lex
from datetime import datetime
import os

# Palabras reservadas en PHP
reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "echo": "ECHO",
    "function": "FUNCTION",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "array": "ARRAY",
    "interface": "INTERFACE",
    "new": "NEW",
    "SplStack": "STACK",
    "SplQueue": "QUEUE",
    "readline": "READLINE",
}

# Lista de nombres de tokens
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
    'QUESTION',
    'DOT',
    'COMA',
    'LBRACKET',
    'RBRACKET',
    'PHP_OPEN',
    'PHP_CLOSE',
    'INPUT',
    'READLINE',
    'NAMEFUNCTION'
) + tuple(reserved.values())

# Reglas de expresiones regulares para tokens simples
t_PHP_OPEN = r'\<\?php'
t_PHP_CLOSE = r'\?\>'
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
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_NOT_OP = r'!'
t_QUESTION = r'\?'
t_DOT = r'\.'
t_COMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Expresión regular para comentarios
def t_COMMENT(t):
    r'(\/\/[^\n]*|\#[^\n]*|\/\*[\s\S]*?\*\/)'
    t.lexer.comments.append(f"Comentario en la linea {t.lineno}: {t.value}")
    pass 

# Expresión regular para números flotantes
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expresión regular para números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Verificación de palabras reservadas e identificadores

#def t_FUNCTION(t):
#    r'[a-zA-Z_][a-zA-Z0-9_]*'
#    t.type = reserved.get(t.value, "FUNCTION")  # Verificar si es palabra reservada
#    return t

def t_NAMEFUNCTION(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, "FUNCTION")  # Verificar si es palabra reservada
    return t

# Patrón para el token INPUT
def t_INPUT(t):
    r'input'
    return t

# Patrón para variables
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Literales de cadenas (comillas simples o dobles)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

# Seguimiento de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    t.lexer.errors.append(f"Caracter ilegal '{t.value[0]}' en la linea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Inicializar atributos personalizados para el lexer
lexer.comments = []  
lexer.errors = []    

# Analizar un archivo y generar logs
def analyze_file(filename, user_git):
    with open(filename, 'r') as file:
        data = file.read()
    
    # Reiniciar comentarios y errores
    lexer.comments = []
    lexer.errors = []

    lexer.input(data)

    # Nombre del archivo de logs
    now = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f'logs/lexer-{user_git}-{now}.txt'

    # Crear carpeta de logs si no existe
    os.makedirs('logs', exist_ok=True)

    # Escribir logs
    with open(log_filename, 'w') as log_file:
        log_file.write(f"Tokens y Errores para {filename}:\n\n")

        while True:
            tok = lexer.token()
            if not tok:
                break
            log_file.write(f"{tok}\n")

        if lexer.comments:
            log_file.write("\nComentarios:\n")
            for comment in lexer.comments:
                log_file.write(f"{comment}\n")

        if lexer.errors:
            log_file.write("\nErrores:\n")
            for error in lexer.errors:
                log_file.write(f"{error}\n")

    print(f"Archivo de log creado: {log_filename}")

# Prueba
if __name__ == "__main__":
    user_git = "sebaescu"
    #analyze_file("algoritmos/fibonacci.php", user_git)

def analyze_Lexico(filename):
    with open(filename, 'r') as file:
        data = file.read()
    
    lexer.comments = []  # Reiniciar comentarios
    lexer.errors = []    # Reiniciar errores

    lexer.input(data)  # Analizar el código PHP

    log_content = ""  # Variable para almacenar el contenido a mostrar

    log_content += f"Tokens y Errores para {filename}:\n\n"

    # Analizar léxicamente
    while True:
        tok = lexer.token()
        if not tok:
            break
        log_content += f"{tok}\n"
    
    if lexer.comments:
        log_content += "\nComentarios:\n"
        for comment in lexer.comments:
            log_content += f"{comment}\n"
    
    if lexer.errors:
        log_content += "\nErrores Léxicos:\n"
        for error in lexer.errors:
            log_content += f"{error}\n"
    
    return log_content  # Retornar el contenido para mostrar en la interfaz