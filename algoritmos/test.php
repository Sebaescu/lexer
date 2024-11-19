<?php
// Declaracion de variables con todos los tipos y almacenar resultados de expresiones/condicionales
$numeroEntero = 10;
$numeroFlotante = 5.75;
$cadena = "Hola, mundo!";
$condicional = ($numeroEntero > $numeroFlotante); // Expresion condicional

// Impresion con cero, uno o más argumentos
echo ""; // Impresion vacia
echo "Un solo argumento"; // Impresion con un argumento
echo $numeroEntero, ", ", $numeroFlotante, ", ", $cadena; // Impresion con multiples argumentos

// Solicitud de datos por teclado 
$entrada = readline("Introduce un valor: "); 
echo "Ingresaste: ", $entrada; 

// Expresiones aritmeticas con uno o mas operadores
$resultadoAritmetico = ($numeroEntero + $numeroFlotante) * 2 - 3 / 2; // Expresion compleja
echo "Resultado de expresión aritmética: ", $resultadoAritmetico;

// Declaracion de un array
$array = array(1, 2, 3, $numeroEntero, $numeroFlotante, $cadena);

// Acceso y modificacion de arrays
$array[0] = 99;
echo "Primer elemento del array modificado: ", $array[0];

// Condiciones con uno o mas conectores
if ($array[0] > 50 && $numeroFlotante < 10 || $condicional) {
    echo "Condición verdadera";
} else {
    echo "Condición falsa";
}

// Declaracion de una funcion

function sumar ( $a, $b ) {
    return $a + $b;
}
/*
// Definicion de una funcion con parametros opcionales y retorno

function dividir($a, $b = 1) {
    if ($b == 0) {
        return "No se puede dividir por cero.";
    }
    return $a / $b;
}

// Llamada a funciones
$resultadoSuma = sumar(5, 3);
echo "Resultado de la suma: ", $resultadoSuma;

$resultadoDivision = dividir(10); // Usando valor por defecto
echo "Resultado de la división: ", $resultadoDivision;

$resultadoDivisionConError = dividir(10, 0); // Dividir por cero
echo "Resultado con error: ", $resultadoDivisionConError;

// Uso de un bucle para recorrer el array (estructura de control adicional)
foreach ($array as $elemento) {
    echo "Elemento del array: ", $elemento;
}
*/
?>