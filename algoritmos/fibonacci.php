<?php
function fibonacci($n) {
    if ($n < 0) {
        return "El numero debe ser mayor o igual a 0";
    } elseif ($n == 0) {
        return 0;
    } elseif ($n == 1) {
        return 1;
    } else {
        $a = 0;
        $b = 1;
        for ($i = 2; $i <= $n; $i++) {
            $temp = $a + $b;
            $a = $b;
            $b = $temp;
        }
        return $b;
    }
}

// Ejemplo 
$position = 4; 
echo "El numero Fibonacci en la posicion $position es: " . fibonacci($position);
?>
