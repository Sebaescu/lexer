<?php
// Función para calcular el factorial de un número
function calcularFactorial($numero) {
    // Validar que el número sea positivo
    if ($numero < 0) {
        return "El número debe ser positivo"; // Retorno en caso de número negativo
    }

    // Si el número es 0, el factorial es 1
    if ($numero === 0) {
        return 1;
    }

    // Inicializar la variable factorial
    $factorial = 1;

    // Calcular el factorial usando un bucle for
    for ($i = 1; $i <= $numero; $i++) {
        $factorial *= $i; // Multiplicación acumulativa
    }

    return $factorial; // Retorno del resultado
}

// Solicitar al usuario un número y calcular el factorial
$numeroUsuario = 5; // Puedes cambiar este valor para probar con otros números
$resultado = calcularFactorial($numeroUsuario);

// Mostrar el resultado al usuario
echo "El factorial de " . $numeroUsuario . " es: " . $resultado;
