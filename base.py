import networkx as nx
import random
import py5
import time

n = 9 # Tamaño del laberinto
jugador_pos = (0, 0)
inicio = (0, 0)
salida = (n - 1, n - 1)
tiempo_inicio = time.time()
tiempo_limite = 50  # Tiempo límite de 50 segundos
en_pausa = False
ganado = False
obstaculos = set()

# Generación de un laberinto más denso con conexiones adicionales
def generar_laberinto(n):
    G = nx.grid_2d_graph(n, n)
    extra_edges = []
    for x in range(n - 1):
        for y in range(n - 1):
            if random.random() > 0.3:
                extra_edges.append(((x, y), (x + 1, y)))
            if random.random() > 0.3:
                extra_edges.append(((x, y), (x, y + 1)))
    G.add_edges_from(extra_edges)
    return G

laberinto = generar_laberinto(n)

# Generación de obstáculos asegurando un camino al final
def generar_obstaculos(n):
    obstaculos.clear()
    # Generar obstáculos de manera aleatoria
    while len(obstaculos) < int(n * 1.5):  # Número de obstáculos ajustado
        x, y = random.randint(0, n-1), random.randint(0, n-1)
        if (x, y) != inicio and (x, y) != salida:
            obstaculos.add((x, y))
    
    # Asegurarse de que hay un camino desde el inicio a la salida
    camino = nx.shortest_path(laberinto, source=inicio, target=salida)
    for nodo in camino[1:-1]:  # No obstruir el inicio y la salida
        obstaculos.discard(nodo)

generar_obstaculos(n)

# Configuración inicial de py5
def setup():
    py5.size(600, 600)  # Tamaño ajustado para el laberinto más grande
    py5.background(135, 206, 235)  # Fondo azul claro que recuerda al cielo
    py5.stroke_weight(2)  # Peso de línea más delgado

# Dibujar el laberinto y el jugador
def draw():
    global tiempo_inicio, ganado

    if en_pausa or ganado:
        return  # No actualizamos si el juego está en pausa o si ya se ha ganado
    
    py5.background(135, 206, 235)  # Fondo azul claro
    dibujar_laberinto(laberinto)
    dibujar_jugador(jugador_pos)
    dibujar_salida()
    dibujar_boton_pausa()
    dibujar_boton_reiniciar()
    
    # Mostrar cronómetro en pantalla
    tiempo_actual = time.time()
    tiempo_restante = max(0, tiempo_limite - int(tiempo_actual - tiempo_inicio))
    py5.fill(255)
    py5.text_size(16)
    py5.text(f"Tiempo restante: {tiempo_restante}s", 10, 20)
    
    # Comprobar si el jugador ha llegado a la salida
    if jugador_pos == salida:
        ganado = True
        mostrar_mensaje_ganado()

    # Mostrar solución si el tiempo se agota
    if tiempo_actual - tiempo_inicio > tiempo_limite:
        mostrar_solucion()

# Dibujar el laberinto usando las aristas del grafo
def dibujar_laberinto(grafo):
    for (nodo1, nodo2) in grafo.edges():
        x1, y1 = nodo1
        x2, y2 = nodo2
        py5.stroke(150, 75, 0)  # Color marrón para el laberinto
        py5.line(x1 * 60 + 30, y1 * 60 + 30, x2 * 60 + 30, y2 * 60 + 30)

# Dibujar al jugador como un círculo rojo
def dibujar_jugador(pos):
    x, y = pos
    py5.fill(255, 0, 0)  # Color rojo para el jugador
    py5.ellipse(x * 60 + 30, y * 60 + 30, 20, 20)

# Dibujar la salida con una etiqueta de "Meta"
def dibujar_salida():
    x, y = salida
    py5.fill(0, 255, 0)  # Color verde para la salida
    py5.rect(x * 60 + 20, y * 60 + 20, 40, 40)
    py5.fill(0)
    py5.text_size(12)
    py5.text("Final", x * 60 + 22, y * 60 + 70)

# Dibujar el botón de pausa
def dibujar_boton_pausa():
    py5.fill(255, 255, 255)  # Botón blanco
    py5.rect(500, 10, 70, 30)
    py5.fill(0)
    py5.text_size(12)
    py5.text("Pausa" if not en_pausa else "Reanudar", 505, 30)

# Dibujar el botón de reiniciar
def dibujar_boton_reiniciar():
    py5.fill(255, 255, 255)  # Botón blanco
    py5.rect(500, 50, 70, 30)
    py5.fill(0)
    py5.text_size(12)
    py5.text("Reiniciar", 505, 70)

# Mostrar la solución en caso de tiempo agotado
def mostrar_solucion():
    py5.stroke(255, 0, 0)
    camino = nx.shortest_path(laberinto, source=inicio, target=salida)
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * 60 + 30, y1 * 60 + 30, x2 * 60 + 30, y2 * 60 + 30)

    # Dibujar la solución más corta en rosa
    py5.stroke(255, 20, 147)  # Color rosa
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * 60 + 30, y1 * 60 + 30, x2 * 60 + 30, y2 * 60 + 30)

# Mostrar mensaje de victoria
def mostrar_mensaje_ganado():
    py5.fill(255, 215, 0)  # Color dorado para resaltar el mensaje
    py5.rect(150, 250, 300, 100)
    py5.fill(0)
    py5.text_size(20)
    py5.text("¡Has ganado!", 230, 300)

# Manejar el movimiento del jugador con las teclas de flechas
def key_pressed():
    global jugador_pos
    if en_pausa or ganado:
        return  # No se mueve el jugador si está en pausa o ya ha ganado
    
    x, y = jugador_pos
    if py5.key == py5.CODED:
        nueva_pos = jugador_pos
        if py5.key_code == py5.UP and (x, y-1) in laberinto.neighbors((x, y)):
            nueva_pos = (x, y-1)
        elif py5.key_code == py5.DOWN and (x, y+1) in laberinto.neighbors((x, y)):
            nueva_pos = (x, y+1)
        elif py5.key_code == py5.LEFT and (x-1, y) in laberinto.neighbors((x, y)):
            nueva_pos = (x-1, y)
        elif py5.key_code == py5.RIGHT and (x+1, y) in laberinto.neighbors((x, y)):
            nueva_pos = (x+1, y)
        
        # Solo mover si la nueva posición no es un obstáculo
        if nueva_pos not in obstaculos:
            jugador_pos = nueva_pos

# Manejar el clic del ratón para pausar/reanudar y reiniciar
def mouse_pressed():
    global en_pausa, tiempo_inicio, jugador_pos, ganado, laberinto

    # Verificar si se ha hecho clic en el botón de pausa
    if 500 <= py5.mouse_x <= 570 and 10 <= py5.mouse_y <= 40:
        en_pausa = not en_pausa
        # Si se reanuda, ajustar el tiempo restante correctamente
        if not en_pausa:
            tiempo_inicio = time.time() - (tiempo_limite - max(0, tiempo_limite - int(time.time() - tiempo_inicio)))
    
    # Verificar si se ha hecho clic en el botón de reiniciar
    if 500 <= py5.mouse_x <= 570 and 50 <= py5.mouse_y <= 80:
        jugador_pos = inicio
        ganado = False
        en_pausa = False
        tiempo_inicio = time.time()
        obstaculos.clear()  # Limpiar obstáculos
        laberinto = generar_laberinto(n)  # Regenerar laberinto
        generar_obstaculos(n)  # Regenerar obstáculos

py5.run_sketch()
