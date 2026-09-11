Simulador de Concurrencia - SIGET

Problema elegido

Productor-consumidor adaptado al SIGET.

Dos sensores de trafico actuan como productores y generan eventos. Un modulo de analisis actua como consumidor y procesa los eventos desde un bufer compartido de capacidad limitada.

Hilos concurrentes

Sensor S1.

Sensor S2.

Modulo de Analisis.

Mecanismos de concurrencia

Semaphore para controlar los espacios libres.

Semaphore para controlar los elementos disponibles.

Lock para exclusion mutua sobre el bufer.

Estos mecanismos evitan que se escriba en un bufer lleno, que se consuma de un bufer vacio y que varios hilos modifiquen simultaneamente la estructura compartida.

Ejecucion

Con Python 3:

python simulador_concurrencia_siget.py

El programa muestra la actividad intercalada de los sensores y del consumidor, el tamano del bufer y el resultado final.

Resultado esperado

12 eventos producidos.

12 eventos consumidos.

0 eventos restantes en el bufer.

Relacion con SIGET

El modelo representa sensores urbanos que generan informacion de trafico y un modulo que analiza esos datos. La sincronizacion permite coordinar la produccion y el consumo de informacion de forma segura.
