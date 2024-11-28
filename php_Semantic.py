from lark import Lark, Transformer, Tree

# Gramática PHP simplificada
php_grammar = """
    start: statement+
    statement: "echo" expr ";"    -> print_stmt
             | "let" VAR "=" expr ";"  -> assign_stmt
    expr: VAR                     -> var_expr
        | NUMBER                  -> number_expr
        | expr "+" expr           -> add_expr
    VAR: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMBER: /\d+/
    %import common.WS
    %ignore WS
"""

class SemanticAnalyzer(Transformer):
    def _init_(self):
        self.symbol_table = {}

    def assign_stmt(self, items):
        var_name = str(items[0])
        value = items[1]
        self.symbol_table[var_name] = value
        return f"Assigned {var_name} = {value}"

    def var_expr(self, items):
        var_name = str(items[0])
        if var_name not in self.symbol_table:
            raise ValueError(f"Variable '{var_name}' not declared.")
        return self.symbol_table[var_name]

    def add_expr(self, items):
        left, right = items
        if not isinstance(left, int) or not isinstance(right, int):
            raise TypeError("Addition only allowed between integers.")
        return left + right

    def number_expr(self, items):
        return int(items[0])

# Crear el analizador
php_parser = Lark(php_grammar, parser='lalr', transformer=SemanticAnalyzer())
code = """
let x = 10;
let y = 20;
echo x + y;
"""

try:
    result = php_parser.parse(code)
    print("Análisis completado exitosamente:", result)
except Exception as e:
    print(f"Error semántico: {e}")