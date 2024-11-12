<?php
function busquedaBinaria($arr, $elemento) {
    $inicio = 0;
    $fin = count($arr) - 1;

    while ($inicio <= $fin) {
        $medio = intval(($inicio + $fin) / 2);
        if ($arr[$medio] == $elemento) {
            return $medio;
        }
        elseif ($arr[$medio] < $elemento) {
            $inicio = $medio + 1;
        }
        else {
            $fin = $medio - 1;
        }
    }
    return -1;
}

$array = [1, 3, 5, 7, 9, 11, 13];
$elementoABuscar = 7;
$indice = busquedaBinaria($array, $elementoABuscar);

if ($indice != -1) {
    echo "Elemento encontrado en el índice: $indice";
} else {
    echo "Elemento no encontrado en el array.";
}
?>