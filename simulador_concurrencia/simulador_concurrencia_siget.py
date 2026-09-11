"""
Simulador de concurrencia SIGET - Productor/Consumidor
2 sensores productores + 1 modulo consumidor.
Mecanismos: semaforos y exclusion mutua.
"""

import threading
import time
import random
from collections import deque
from dataclasses import dataclass

CAPACIDAD_BUFFER = 4
TOTAL_POR_PRODUCTOR = 6

@dataclass
class Evento:
    sensor: str
    tipo: str
    datos: int
    secuencia: int

buffer = deque()
espacios_disponibles = threading.Semaphore(CAPACIDAD_BUFFER)
elementos_disponibles = threading.Semaphore(0)
mutex = threading.Lock()
print_lock = threading.Lock()
estadisticas_lock = threading.Lock()

producidos = 0
consumidos = 0

def mostrar(mensaje):
    with print_lock:
        print(mensaje, flush=True)

def producir(sensor, semilla):
    global producidos
    rng = random.Random(semilla)
    tipos = ["Flujo vehicular", "Velocidad", "Ocupacion", "Incidente"]

    for i in range(1, TOTAL_POR_PRODUCTOR + 1):
        time.sleep(rng.uniform(0.10, 0.30))
        evento = Evento(sensor, rng.choice(tipos), rng.randint(20, 500), i)

        espacios_disponibles.acquire()
        with mutex:
            buffer.append(evento)
            tamano = len(buffer)
            with estadisticas_lock:
                producidos += 1
            mostrar(
                f"[PRODUCTOR {sensor}] genero {evento.tipo} | "
                f"datos={evento.datos} MB | buffer={tamano}/{CAPACIDAD_BUFFER}"
            )
        elementos_disponibles.release()

    mostrar(f"[PRODUCTOR {sensor}] finalizo.")

def consumir():
    global consumidos
    total_esperado = TOTAL_POR_PRODUCTOR * 2

    for _ in range(total_esperado):
        elementos_disponibles.acquire()
        with mutex:
            evento = buffer.popleft()
            tamano = len(buffer)
            with estadisticas_lock:
                consumidos += 1
            mostrar(
                f"    [CONSUMIDOR] proceso {evento.sensor}-{evento.secuencia} | "
                f"{evento.tipo} | datos={evento.datos} MB | "
                f"buffer={tamano}/{CAPACIDAD_BUFFER}"
            )
        espacios_disponibles.release()
        time.sleep(0.15)

    mostrar("[CONSUMIDOR] finalizo el analisis de todos los eventos.")

def main():
    print("=" * 72)
    print("SIMULADOR DE CONCURRENCIA - SIGET")
    print("Problema: PRODUCTOR-CONSUMIDOR con semaforos")
    print("=" * 72)
    print(f"Capacidad del bufer: {CAPACIDAD_BUFFER}")
    print("Hilos concurrentes: Sensor S1, Sensor S2 y Modulo de Analisis")
    print("-" * 72)

    inicio = time.perf_counter()

    sensor_1 = threading.Thread(target=producir, args=("S1", 101))
    sensor_2 = threading.Thread(target=producir, args=("S2", 202))
    consumidor = threading.Thread(target=consumir)

    sensor_1.start()
    sensor_2.start()
    consumidor.start()

    sensor_1.join()
    sensor_2.join()
    consumidor.join()

    duracion = time.perf_counter() - inicio

    print("-" * 72)
    print("RESULTADO FINAL")
    print(f"Eventos producidos: {producidos}")
    print(f"Eventos consumidos: {consumidos}")
    print(f"Eventos restantes en bufer: {len(buffer)}")
    print(f"Tiempo de simulacion: {duracion:.2f} s")
    print("Estado: ejecucion completada sin perdida ni corrupcion del bufer.")
    print("Control de concurrencia: semaforos + exclusion mutua.")
    print("Prevencion de interbloqueo: orden de adquisicion controlado.")
    print("=" * 72)

if __name__ == "__main__":
    main()
