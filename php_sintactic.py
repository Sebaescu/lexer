import ply.yacc as yacc
from php_Lexer import tokens
import os
import logging
from datetime import datetime

# Precedencia para resolver conflictos
precedence = (
    ('left', 'OR_OP'),
    ('left', 'AND_OP'),
    ('left', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT_OP'),
    ('right', 'READLINE'),
    ('right', 'ASSIGN'),
    ('right', 'ELSE'),
)


# Bloque principal de PHP
def p_php_block(p):
    '''php_block : PHP_OPEN statement_list PHP_CLOSE'''


# Lista de declaraciones o sentencias
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

def p_statement(p):
    '''statement : asignacion
                 | impresion
                 | if_statement
                 | funcion
                 | declarar_array
                 | retorno
                 | input_statement
                 | for_statement
                 | empty
                 '''

# Leer entrada desde teclado
def p_input_statement(p):
    '''input_statement : VARIABLE ASSIGN READLINE LPAREN STRING RPAREN SEMICOL'''


# Definición de una función
def p_funcion(p):
    '''funcion : FUNCTION NAMEFUNCTION LPAREN parametros RPAREN LBRACE statement_list RBRACE'''

# Asignación
def p_asignacion(p):
    '''asignacion : VARIABLE ASSIGN expresion SEMICOL
                  | VARIABLE ASSIGN condicion SEMICOL
                  | array_access ASSIGN expresion SEMICOL'''



# Impresión
def p_impresion(p):
    '''impresion : ECHO SEMICOL
                 | ECHO expresion SEMICOL
                 | ECHO expresion_list SEMICOL'''


def p_expresion_list(p):
    '''expresion_list : expresion
                      | expresion COMA expresion_list'''


# Expresión
def p_expresion(p):
    '''expresion : termino
                 | termino operador expresion
                 | termino comparador termino
                 | LPAREN expresion RPAREN operador expresion
                 | LPAREN expresion RPAREN
                 | llamada_funcion
                 | array_access'''


# Términos
def p_termino(p):
    '''termino : VARIABLE
               | NUMBER
               | FLOAT
               | STRING'''



# Condición
def p_condicion(p):
    '''condicion : expresion comparador expresion
                 | condicion AND_OP condicion
                 | condicion OR_OP condicion
                 | NOT_OP condicion
                 | expresion'''


# Comparadores
def p_comparador(p):
    '''comparador : EQ
                  | NEQ
                  | GT
                  | LT
                  | GE
                  | LE'''


# Operadores
def p_operador(p):
    '''operador : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | MOD'''


# Condición if/else/elseif
def p_if_statement(p):
    '''if_statement : IF LPAREN condicion RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN condicion RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN condicion RPAREN LBRACE statement_list RBRACE elseif_blocks ELSE LBRACE statement_list RBRACE'''

def p_elseif_blocks(p):
    '''elseif_blocks : ELSEIF LPAREN condicion RPAREN LBRACE statement_list RBRACE
                     | elseif_blocks ELSEIF LPAREN condicion RPAREN LBRACE statement_list RBRACE'''

def p_for_statement(p):
    '''for_statement : FOR LPAREN initialization SEMICOL condition SEMICOL increment RPAREN LBRACE statement_list RBRACE'''

# Inicialización del bucle
def p_initialization(p):
    '''initialization : VARIABLE ASSIGN expresion
                      | initialization COMA VARIABLE ASSIGN expresion
                      | empty'''

# Condición del bucle
def p_condition(p):
    '''condition : expresion comparador expresion'''

# Incremento del bucle
def p_increment(p):
    '''increment : VARIABLE PLUS PLUS
                 | VARIABLE MINUS MINUS
                 | VARIABLE ASSIGN expresion'''

# Inicialización del bucle
def p_initialization(p):
    '''initialization : VARIABLE ASSIGN expresion
                      | initialization COMA VARIABLE ASSIGN expresion'''

# Condición del bucle
def p_condition(p):
    '''condition : expresion comparador expresion'''

# Incremento del bucle
def p_increment(p):
    '''increment : VARIABLE INCREMENT
                 | VARIABLE DECREMENT'''
    
def p_parametros(p):
    '''parametros : VARIABLE
                  | VARIABLE COMA parametros
                  | empty'''


# Declaración de un array
def p_declarar_array(p):
    '''declarar_array : VARIABLE ASSIGN ARRAY LPAREN argumentos RPAREN SEMICOL
                      | VARIABLE ASSIGN LBRACKET argumentos RBRACKET SEMICOL'''


def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos
                  | empty'''


# Retorno
def p_retorno(p):
    '''retorno : RETURN expresion SEMICOL'''


# Llamada a función
def p_llamada_funcion(p):
    '''llamada_funcion : VARIABLE LPAREN argumentos RPAREN'''



# Acceso a arrays
def p_array_access(p):
    '''array_access : VARIABLE LBRACKET expresion RBRACKET'''


# Producción vacía
def p_empty(p):
    '''empty :'''


# Manejo de errores
def p_error(p):
    if p:
        error_message = f"Error de sintaxis en la linea {p.lineno}, token inesperado: {p.value}"
        logging.error(error_message)
        print(error_message)
        raise SyntaxError(error_message)  
    else:
        error_message = "Error de sintaxis al final del archivo."
        logging.error(error_message)
        print(error_message)
        raise SyntaxError(error_message)

# Construcción del parser
parser = yacc.yacc()

# Análisis y generación de logs
def analyze_php_file_with_logs(filename, user_git):
    with open(filename, 'r') as file:
        data = file.read()

    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)

    now = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = os.path.join(log_folder, f"sintactico-{user_git}-{now}.txt")

    logging.basicConfig(level=logging.DEBUG, filename=log_filename, filemode='w',
                        format='%(message)s')

    # Ejecutar el análisis sintáctico
    try:
        result = parser.parse(data, debug=logging)
        print(f"Analisis completado. Revisa el log en {log_filename}")
    except SyntaxError:
        print(f"Errores detectados durante el analisis. Revisa el log en {log_filename}")
    except Exception as e:
        error_message = f"Error inesperado al analizar el archivo: {e}"
        logging.error(error_message)
        print(error_message)

# Prueba
if __name__ == "__main__":
    user_git = "kgjara"
    analyze_php_file_with_logs("algoritmos/fibonacci.php", user_git)
