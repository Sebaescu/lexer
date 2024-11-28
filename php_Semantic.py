from lark import Lark, Transformer, Tree

# Gramática PHP simplificada para el análisis semántico
php_grammar = """
    start: statement+
    statement: "echo" expr ";"                          -> print_stmt
             | "let" VAR "=" expr ";"                  -> assign_stmt
             | "if" expr "{" statement+ "}"            -> if_stmt
             | "elseif" expr "{" statement+ "}"        -> elseif_stmt
             | "else" "{" statement+ "}"               -> else_stmt
             | "return" expr ";"                       -> return_stmt
             | "function" VAR "(" params ")" "{" statement+ "}" -> function_stmt
    expr: VAR                                           -> var_expr
        | NUMBER                                        -> number_expr
        | expr "+" expr                                 -> add_expr
        | expr "<" expr                                 -> lt_expr
        | expr "==" expr                                -> eq_expr
        | expr ">" expr                                 -> gt_expr
    VAR: /[a-zA-Z_][a-zA-Z0-9_]*/                        -> var
    NUMBER: /\d+/                                       -> number
    params: VAR ("," VAR)*
    %import common.WS
    %ignore WS
"""

# Clases de análisis semántico
class SemanticAnalyzer(Transformer):
    def __init__(self):
        self.symbol_table = {}  # Tabla de símbolos para almacenar variables
        self.log = []  # Log de resultados

    def assign_stmt(self, items):
        var_name = str(items[0])  # Obtener el nombre de la variable
        value = items[1]  # Obtener el valor que se asigna
        if not isinstance(value, int):
            raise ValueError(f"Error: La asignación de la variable '{var_name}' debe ser de un valor entero.")
        self.symbol_table[var_name] = value  # Guardar en la tabla de símbolos
        self.log.append(f"Variable '{var_name}' asignada con el valor {value}")
        return f"Variable '{var_name}' asignada con el valor {value}"

    def var_expr(self, items):
        var_name = str(items[0])  # Obtener el nombre de la variable
        if var_name not in self.symbol_table:
            raise ValueError(f"Error semántico: La variable '{var_name}' no está declarada.")  # Error si la variable no está declarada
        return self.symbol_table[var_name]

    def add_expr(self, items):
        left, right = items  # Obtener los dos operandos
        if not isinstance(left, int) or not isinstance(right, int):
            raise TypeError("Error semántico: La operación de suma solo es válida para enteros.")
        result = left + right
        self.log.append(f"Operación de suma: {left} + {right} = {result}")
        return result

    def number_expr(self, items):
        return int(items[0])  # Convertir el valor numérico a entero

    def lt_expr(self, items):
        left, right = items
        if not isinstance(left, int) or not isinstance(right, int):
            raise TypeError("Error semántico: La operación '<' solo es válida para enteros.")
        return left < right

    def eq_expr(self, items):
        left, right = items
        if not isinstance(left, int) or not isinstance(right, int):
            raise TypeError("Error semántico: La operación '==' solo es válida para enteros.")
        return left == right

    def gt_expr(self, items):
        left, right = items
        if not isinstance(left, int) or not isinstance(right, int):
            raise TypeError("Error semántico: La operación '>' solo es válida para enteros.")
        return left > right

    def if_stmt(self, items):
        condition = items[0]
        if not isinstance(condition, bool):
            raise TypeError("Error semántico: La condición del 'if' debe ser un valor booleano.")
        self.log.append(f"Condición 'if' evaluada: {condition}")
        return items  # Si la condición es válida, se procesan las sentencias dentro del bloque

    def function_stmt(self, items):
        function_name = str(items[0])
        self.symbol_table[function_name] = "function"  # Marcar que la función está declarada
        self.log.append(f"Función '{function_name}' declarada.")
        return f"Función '{function_name}' declarada."

# Crear el analizador con la gramática definida
php_parser = Lark(php_grammar, parser='lalr', transformer=SemanticAnalyzer())

# Función para ejecutar el análisis semántico y retornar el log
def analyze_php_semantic(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()  # Leer el contenido del archivo PHP
        # Realizar el análisis semántico
        result = php_parser.parse(code)  # Ejecutar el análisis semántico
        return '\n'.join(result.log)  # Unir los logs y retornarlos como una cadena
    except Exception as e:
        return f"Error semántico: {e}"

