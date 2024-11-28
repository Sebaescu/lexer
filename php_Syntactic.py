import ply.yacc as yacc
from php_Lexer import tokens
import os
import logging
from datetime import datetime


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()

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
    pass

# Lista de declaraciones o sentencias
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    pass
# Leer entrada desde teclado
def p_input_statement(p):
    '''input_statement : VARIABLE ASSIGN READLINE LPAREN STRING RPAREN SEMICOL'''
    pass

# Definición de una función
def p_funcion(p):
    '''funcion : FUNCTION NAMEFUNCTION LPAREN parametros RPAREN LBRACE statement_list RBRACE'''
    pass

def p_statement(p):
    '''statement : asignacion
                 | impresion
                 | if_statement
                 | funcion
                 | declarar_array
                 | retorno
                 | input_statement'''  
    pass

# Asignación
def p_asignacion(p):
    '''asignacion : VARIABLE ASSIGN expresion SEMICOL
                  | VARIABLE ASSIGN condicion SEMICOL
                  | array_access ASSIGN expresion SEMICOL'''
    pass


# Impresión
def p_impresion(p):
    '''impresion : ECHO SEMICOL
                 | ECHO expresion SEMICOL
                 | ECHO expresion_list SEMICOL'''
    pass

def p_expresion_list(p):
    '''expresion_list : expresion
                      | expresion COMA expresion_list'''
    pass

# Expresión
def p_expresion(p):
    '''expresion : termino
                 | termino operador expresion
                 | termino comparador termino
                 | LPAREN expresion RPAREN operador expresion
                 | LPAREN expresion RPAREN
                 | llamada_funcion
                 | array_access'''
    pass

# Términos
def p_termino(p):
    '''termino : VARIABLE
               | NUMBER
               | FLOAT
               | STRING'''
    pass


# Condición
def p_condicion(p):
    '''condicion : expresion comparador expresion
                 | condicion AND_OP condicion
                 | condicion OR_OP condicion
                 | NOT_OP condicion
                 | expresion'''
    pass

# Comparadores
def p_comparador(p):
    '''comparador : EQ
                  | NEQ
                  | GT
                  | LT
                  | GE
                  | LE'''
    pass

# Operadores
def p_operador(p):
    '''operador : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | MOD'''
    pass

# Condición if
def p_if_statement(p):
    '''if_statement : IF LPAREN condicion RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN condicion RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE %prec ELSE'''
    pass

def p_parametros(p):
    '''parametros : VARIABLE
                  | VARIABLE COMA parametros
                  | empty'''
    pass

# Declaración de un array
def p_declarar_array(p):
    '''declarar_array : VARIABLE ASSIGN ARRAY LPAREN argumentos RPAREN SEMICOL
                      | VARIABLE ASSIGN LBRACKET argumentos RBRACKET SEMICOL'''
    pass

def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos
                  | empty'''
    pass

# Retorno
def p_retorno(p):
    '''retorno : RETURN expresion SEMICOL'''
    pass

# Llamada a función
def p_llamada_funcion(p):
    '''llamada_funcion : VARIABLE LPAREN argumentos RPAREN'''
    pass


# Acceso a arrays
def p_array_access(p):
    '''array_access : VARIABLE LBRACKET expresion RBRACKET'''
    pass

# Producción vacía
def p_empty(p):
    '''empty :'''
    pass

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
parser = yacc.yacc(debug=True, debuglog=logger)

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
    user_git = "sebaescu"
    analyze_php_file_with_logs("algoritmos/fibonacci.php", user_git)

def analyze_sintactico(filename):
    with open(filename, 'r') as file:
        data = file.read()

    log_content = ""  # Para almacenar el contenido a mostrar en el área de texto

    try:
        # Ejecutar el análisis sintáctico con depuración
        result = parser.parse(data)  # 'parser' es tu analizador sintáctico
        log_content += f"Análisis sintáctico completado correctamente para {filename}.\n\n"
        log_content += "Resultado del análisis sintáctico:\n"
        log_content += str(result)  # Mostrar los resultados del análisis (esto dependerá de tu parser)
    except SyntaxError as e:
        # Capturamos el error de sintaxis y lo mostramos
        log_content += f"Error de sintaxis: {str(e)}\n"
    except Exception as e:
        log_content += f"Error inesperado al analizar el archivo: {e}\n"

    return log_content  # Retornar el contenido para mostrar en la interfaz
