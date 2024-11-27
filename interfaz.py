import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from php_Lexer import analyze_Lexico  # Asegúrate de que esta función esté correctamente importada
from php_Syntactic import analyze_sintactico  # Asegúrate de que esta función esté correctamente importada
import os

# Crear una instancia de la ventana principal de Tkinter
root = tk.Tk()
root.title("Analizador de Lenguaje PHP")
root.state('zoomed')  # Ventana maximizada al iniciar

# Crear un área de texto donde se mostrarán los resultados
output_text = scrolledtext.ScrolledText(root, width=100, height=30, wrap=tk.WORD)
output_text.pack(pady=10)

# Variable global para almacenar el código y nombre del archivo
code_content = ""
file_name = ""

# Función para abrir un archivo PHP
def open_file():
    global file_name, code_content
    
    file_path = filedialog.askopenfilename(filetypes=[("Archivos PHP", "*.php")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                code_content = file.read()
            file_name = os.path.basename(file_path)  # Solo el nombre del archivo
            file_label.config(text=f"Archivo seleccionado: {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

# Función para mostrar los resultados del log en el área de texto
def display_log_results(log_content):
    output_text.delete(1.0, tk.END)  # Limpiar el área de texto antes de agregar nuevos resultados
    output_text.insert(tk.END, log_content)  # Mostrar el contenido del log en el área de texto

# Nueva función para analizar léxicamente el archivo y mostrar resultados en pantalla
def handle_lexico_analysis(filename):
    if not filename:
        messagebox.showerror("Error", "No se ha cargado ningún archivo.")
        return
    
    try:
        # Llamada a la función analyze_Lexico del archivo php_Lexer.py
        log_content = analyze_Lexico(f"algoritmos/{filename}")
        display_log_results(log_content)  # Mostrar los resultados del análisis léxico en pantalla
    except Exception as e:
        messagebox.showerror("Error", f"Error al analizar léxico: {str(e)}")

# Nueva función para analizar sintácticamente el archivo y mostrar resultados en pantalla
def handle_sintactico_analysis(filename):
    if not filename:
        messagebox.showerror("Error", "No se ha cargado ningún archivo.")
        return
    
    try:
        # Llamada a la función analyze_sintactico del archivo php_Syntactic.py
        log_content = analyze_sintactico(f"algoritmos/{filename}")
        display_log_results(log_content)  # Mostrar los resultados del análisis sintáctico en pantalla
    except SyntaxError as e:
        # Mostrar el error de sintaxis en el área de texto
        log_content = f"Error de sintaxis: {str(e)}"
        display_log_results(log_content)  # Mostrar el mensaje de error en el área de texto
    except Exception as e:
        messagebox.showerror("Error", f"Error al analizar sintáctico: {str(e)}")

# Función para ejecutar el análisis basado en la opción seleccionada
def analyze_selected_type(analysis_type):
    if not code_content:
        messagebox.showerror("Error", "No se ha cargado ningún archivo.")
        return
    
    if analysis_type == "léxico":
        handle_lexico_analysis(file_name)  # Llamar a la nueva función handle_lexico_analysis
    elif analysis_type == "sintáctico":
        handle_sintactico_analysis(file_name)  # Llamar a la nueva función handle_sintactico_analysis
    elif analysis_type == "semántico":
        analyze_semantic(code_content)
    else:
        messagebox.showerror("Error", "Tipo de análisis no reconocido.")

# Función para crear la interfaz de los botones y el menú
def create_buttons():
    # Frame para los botones
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Botón para abrir el archivo PHP
    open_button = tk.Button(button_frame, text="Abrir Archivo PHP", command=open_file, height=2, width=20)
    open_button.grid(row=0, column=0, padx=10)

    # Etiqueta para mostrar el nombre del archivo
    global file_label
    file_label = tk.Label(button_frame, text="Archivo seleccionado: Ninguno", height=2, width=50)
    file_label.grid(row=0, column=1, padx=10)

    # Menú para seleccionar el tipo de análisis
    analysis_frame = tk.Frame(root)
    analysis_frame.pack(pady=10)

    lexical_button = tk.Button(analysis_frame, text="Análisis Léxico", command=lambda: analyze_selected_type("léxico"), height=2, width=20)
    lexical_button.grid(row=0, column=0, padx=10)

    syntactic_button = tk.Button(analysis_frame, text="Análisis Sintáctico", command=lambda: analyze_selected_type("sintáctico"), height=2, width=20)
    syntactic_button.grid(row=0, column=1, padx=10)

    semantic_button = tk.Button(analysis_frame, text="Análisis Semántico", command=lambda: analyze_selected_type("semántico"), height=2, width=20)
    semantic_button.grid(row=0, column=2, padx=10)

# Crear los botones
create_buttons()

# Ejecutar la interfaz
root.mainloop()
