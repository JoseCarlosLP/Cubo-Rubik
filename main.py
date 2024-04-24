import copy
import time
from queue import PriorityQueue


class Cara:
    def __init__(self, color):
        self.piezas = [[color for _ in range(3)] for _ in range(3)]
        self.centro = self.piezas[1][1]

    def mostrar_piezas(self):
        for i in range(3):
            for j in range(3):
                print(self.piezas[i][j],end=' ')
            print()

    def set_centro(self,color):
        self.centro = color

    def set_color_a_pieza(self, i, j, color):
        self.piezas[i][j] = color

    def esta_resuelto(self):
        # color = self.piezas[2][2]
        for i in range(len(self.piezas)):
            for j in range(len(self.piezas[i])):
                if self.piezas[i][j] != self.centro:
                # if self.piezas[i][j][0] != self.centro or self.piezas[i][j][1] != i or self.piezas[i][j][2] != j:
                    return False
        return True

    def __eq__(self, other):
        return self.piezas == other.piezas

    def __lt__(self, other):
        return self.piezas < other.piezas

    def contar_piezas_de_color_diferente_al_centro(self):
        total = 9
        for i in range(len(self.piezas)):
            for j in range(len(self.piezas[i])):
                if self.piezas[i][j] == self.centro:
                    total -= 1
        # print(total)
        return total

    def contar_esquinas_correctas(self):
        total = 0
        for fila in self.piezas:
            if fila[0] == self.centro:
                if fila[-1] == self.centro:
                    total += 2
                else:
                    total += 1
        return total


class CuboRubik:
    def __init__(self):
        self.caras = {
            'U': Cara('W'),
            'D': Cara('Y'),
            'L': Cara('O'),
            'F': Cara('G'),
            'R': Cara('R'),
            'B': Cara('B')
        }
        self.acciones = {
            'F': lambda: self.girar_cara_frontal(),
            "F'": lambda: self.girar_cara_frontal('antihorario'),
            'B': lambda: self.girar_cara_posterior(),
            "B'": lambda: self.girar_cara_posterior('antihorario'),
            'U': lambda: self.girar_cara_superior(),
            "U'": lambda: self.girar_cara_superior('antihorario'),
            'D': lambda: self.girar_cara_inferior(),
            "D'": lambda: self.girar_cara_inferior('antihorario'),
            'L': lambda: self.girar_cara_izquierda(),
            "L'": lambda: self.girar_cara_izquierda('antihorario'),
            'R': lambda: self.girar_cara_derecha(),
            "R'": lambda: self.girar_cara_derecha('antihorario'),
            # 'M': lambda: self.girar_cara_m(),
            # "M'": lambda: self.girar_cara_m('antihorario'),
            # 'S': lambda: self.girar_cara_s(),
            # "S'": lambda: self.girar_cara_s('antihorario'),
            # 'E': lambda: self.girar_cara_e(),
            # "E'": lambda: self.girar_cara_e('antihorario')
        }
        self.cubo_padre = None
        self.movimiento_padre = None

    def revisar_fila(self, fila, cantidad_colores):
        if len(fila) == 3:
            for i in range(len(fila)):
                if fila[i] not in ['W', 'Y', 'O', 'G', 'R', 'B']:
                    return False
                cantidad_colores[fila[i]] += 1
        else:
            return False
        return True

    def revisar_cantidad_colores(self, cantidad_colores):
        for valor in cantidad_colores.values():
            if valor > 9 or valor <= 0:
                return False
        return True

    def cargar_cubo_desde_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'r') as archivo:
                contenido = archivo.readlines()
                colores_centros = set()
                cantidad_colores = {'W': 0, 'Y': 0, 'O': 0, 'G': 0, 'R': 0, 'B': 0}
                i = 0
                for cara in self.caras:
                    fila_superior = [fila.strip().split() for fila in contenido[i].split(',')]
                    fila_central = [fila.strip().split() for fila in contenido[i + 1].split(',')]
                    fila_inferior = [fila.strip().split() for fila in contenido[i + 2].split(',')]
                    if not self.revisar_fila(fila_superior[0], cantidad_colores) or not self.revisar_fila(
                            fila_central[0],
                            cantidad_colores) or not self.revisar_fila(
                        fila_inferior[0], cantidad_colores):
                        print("Color de pieza introducido incorrecto o cantidad de piezas introducidas en la fila "
                              "incorrecta")
                        return False
                    if fila_central[0][1] not in colores_centros:
                        colores_centros.add(fila_central[0][1])
                        self.caras[cara].set_centro(fila_central[0][1])
                        self.caras[cara].piezas[0] = fila_superior[0]
                        self.caras[cara].piezas[1] = fila_central[0]
                        self.caras[cara].piezas[2] = fila_inferior[0]
                        i = i + 3
                    else:
                        print("Se estan repitiendo los colores de mas de un centro!")
                        return False
                if not self.revisar_cantidad_colores(cantidad_colores):
                    print("Cantidad de piezas de un mismo color invalida")
                    return False
        except FileNotFoundError:
            print(f"El archivo '{nombre_archivo}' no se encontró.")
            return False

        return True

    def total_piezas_diferentes_a_su_centro(self):
        cont = 0
        for cara in self.caras:
            cont += self.caras[cara].contar_piezas_de_color_diferente_al_centro()
        return cont
        # IDEA: Talvez verificar si las filas de cada cara es toda igual, si no es, nos enfocamos en giros L,R,...
        # cont = 0
        # for cara in self.caras:
        #     cont += self.caras[cara].contar_esquinas_correctas()
        # return cont

    def get_acciones(self):
        if self.movimiento_padre is not None:
            movimientos = {"F": "F'", "F'": "F", "B": "B'", "B'": "B", "R": "R'", "R'": "R", "L": "L'", "L'": "L",
                           "U": "U'", "U'": "U", "D": "D'", "D'": "D", "M": "M'", "M'": "M", "S": "S'", "S'": "S",
                           "E": "E'", "E'": "E"}
            self.acciones.pop(movimientos[self.movimiento_padre])
        return self.acciones

    def set_padre_y_mov_padre(self, padre, movimiento):
        self.cubo_padre = padre
        self.movimiento_padre = movimiento

    def __hash__(self):
        colores = []
        for cara in self.caras.values():
            for fila in cara.piezas:
                for pieza in fila:
                    colores.append(pieza)
        return hash(tuple(colores))

    def toString(self):
        colores = ""
        for cara in self.caras.values():
            for fila in cara.piezas:
                for pieza in fila:
                    colores += str(pieza)
        return colores

    def __eq__(self, other):
        return self.caras == other.caras

    def __lt__(self, other):
        return self.total_piezas_diferentes_a_su_centro() < other.total_piezas_diferentes_a_su_centro()

    def girar_cara_actual(self, cara, sentido='horario'):
        a = 2
        b = 0
        if sentido == 'antihorario':
            a = 0
            b = 2
        esquinas = [[0, 0], [a, b], [2, 2], [b, a]]
        centros = [[0, 1], [1, b], [2, 1], [1, a]]
        tmp_esquina = self.caras[cara].piezas[esquinas[0][0]][esquinas[0][1]]
        tmp_centro = self.caras[cara].piezas[centros[0][0]][centros[0][1]]
        for i in range(3):
            self.caras[cara].set_color_a_pieza(esquinas[i][0], esquinas[i][1],
                                               self.caras[cara].piezas[esquinas[i + 1][0]][
                                                   esquinas[i + 1][1]])
            self.caras[cara].set_color_a_pieza(centros[i][0], centros[i][1], self.caras[cara].piezas[centros[i + 1][0]][
                centros[i + 1][1]])

        self.caras[cara].set_color_a_pieza(esquinas[3][0], esquinas[3][1], tmp_esquina)
        self.caras[cara].set_color_a_pieza(centros[3][0], centros[3][1], tmp_centro)

    def girar_cara_F_B_S(self, a, b, sentido):
        if sentido == 'horario':
            temp_cara_u = [fila[a] for fila in self.caras['L'].piezas]
            temp_cara_lado = [fila[b] for fila in self.caras['R'].piezas]
            for i in range(len(self.caras['L'].piezas)):
                self.caras['L'].piezas[i][a] = self.caras['D'].piezas[b][i]
                self.caras['R'].piezas[i][b] = self.caras['U'].piezas[a][i]
            self.caras['D'].piezas[b] = temp_cara_lado[::-1]
            self.caras['U'].piezas[a] = temp_cara_u[::-1]
        elif sentido == 'antihorario':
            temp_cara_u = self.caras['U'].piezas[a]
            self.caras['U'].piezas[a] = [fila[b] for fila in self.caras['R'].piezas]
            temp_cara_lado = [fila[a] for fila in self.caras['L'].piezas]
            for i in range(len(self.caras['R'].piezas)):
                self.caras['R'].piezas[i][b] = self.caras['D'].piezas[b][-(i + 1)]
                self.caras['L'].piezas[i][a] = temp_cara_u[-(i + 1)]
            self.caras['D'].piezas[b] = temp_cara_lado

    def girar_cara_frontal(self, sentido='horario'):
        self.girar_cara_actual('F', sentido)
        self.girar_cara_F_B_S(-1, 0, sentido)

    def girar_cara_s(self, sentido='horario'):
        self.girar_cara_F_B_S(1, 1, sentido)

    def girar_cara_posterior(self, sentido='horario'):
        self.girar_cara_actual('B', sentido)
        if sentido == 'horario':
            sentido = 'antihorario'
        else:
            sentido = 'horario'
        self.girar_cara_F_B_S(0, -1, sentido)

    def girar_cara_L_M_R(self, a, b, sentido):
        orden = ['B', 'D', 'F', 'U']
        if sentido == 'antihorario':
            orden = ['B', 'U', 'F', 'D']
        temp_cara = [fila[b] for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].set_color_a_pieza(-(i + 1), b, self.caras[orden[1]].piezas[i][a])
            self.caras[orden[1]].set_color_a_pieza(i, a, self.caras[orden[2]].piezas[i][a])
            self.caras[orden[2]].set_color_a_pieza(i, a, self.caras[orden[3]].piezas[i][a])
            self.caras[orden[3]].set_color_a_pieza(i, a, temp_cara[-(i + 1)])

    def girar_cara_derecha(self, sentido='horario'):
        self.girar_cara_actual('R', sentido)
        if sentido == 'horario':
            sentido = 'antihorario'
        else:
            sentido = 'horario'
        self.girar_cara_L_M_R(-1, 0, sentido)

    def girar_cara_izquierda(self, sentido='horario'):
        self.girar_cara_actual('L', sentido)
        self.girar_cara_L_M_R(0, -1, sentido)

    def girar_cara_m(self, sentido='horario'):
        self.girar_cara_L_M_R(1, 1, sentido)

    def girar_cara_U_D_E(self, a, sentido):
        orden = ['F', 'L', 'B', 'R']
        if sentido == 'antihorario':
            orden = ['F', 'R', 'B', 'L']
        temp_cara = self.caras[orden[0]].piezas[a]
        self.caras[orden[0]].piezas[a] = self.caras[orden[1]].piezas[a]
        self.caras[orden[1]].piezas[a] = self.caras[orden[2]].piezas[a]
        self.caras[orden[2]].piezas[a] = self.caras[orden[3]].piezas[a]
        self.caras[orden[3]].piezas[a] = temp_cara

    def girar_cara_superior(self, sentido='horario'):
        self.girar_cara_actual('U', sentido)
        if sentido == 'horario':
            sentido = 'antihorario'
        else:
            sentido = 'horario'
        self.girar_cara_U_D_E(0, sentido)

    def girar_cara_inferior(self, sentido='horario'):
        self.girar_cara_actual('D', sentido)
        self.girar_cara_U_D_E(-1, sentido)

    def girar_cara_e(self, sentido='horario'):
        self.girar_cara_U_D_E(1, sentido)

    def mostrar_estado(self):
        print("CUBO RUBIK")
        for cara in self.caras:
            print(f"Cara {cara}:")
            for fila in self.caras[cara].piezas:
                print(" ".join([str(pieza) for pieza in fila]))
            print()

    def pruebas(self):
        self.girar_cara_inferior()
        self.girar_cara_superior()
        self.girar_cara_inferior()
        self.girar_cara_superior()

        self.girar_cara_derecha()
        self.girar_cara_derecha()
        self.girar_cara_posterior('antihorario')
        self.girar_cara_superior()
        self.girar_cara_superior()
        self.girar_cara_frontal()
        self.girar_cara_izquierda('antihorario')
        self.girar_cara_izquierda('antihorario')
        self.girar_cara_inferior('antihorario')

    def esta_resuelto(self):
        for cara in self.caras:
            if not self.caras[cara].esta_resuelto():
                return False
        return True


class Frontier:
    def __init__(self):
        self.values = []

    def push(self, value):
        self.values.append(value)

    def has(self, value):
        return value in self.values

    def is_empty(self):
        return len(self.values) == 0


class Queue(Frontier):
    def pop(self):
        return self.values.pop(0)


CARAS = {'F': 1, 'B': 2, 'U': 3, 'D': 4, 'L': 5, 'R': 6}


class Searcher:
    def __init__(self, estado_inicial):
        self.estado_inicial = estado_inicial

    def breadth_first(self):
        return self.search(self.estado_inicial, frontier=Queue())

    def search(self, initial_state, frontier):
        frontier.push(initial_state)
        visitados = set(initial_state.toString())
        # i = 1
        while not frontier.is_empty() and not initial_state.esta_resuelto():
            # print("# ESTADOS VISITADOS  = ", i)
            # i = i + 1
            estado_actual = frontier.pop()
            for movimiento in estado_actual.get_acciones():
                sig_cubo_caras = copy.deepcopy(estado_actual.caras)
                sig_estado = CuboRubik()
                sig_estado.caras = sig_cubo_caras
                # print(action)
                sig_estado.acciones[movimiento]()
                # next_cubo.mostrar_estado()
                if sig_estado.esta_resuelto():
                    # print("RESUELTO")
                    sig_estado.set_padre_y_mov_padre(estado_actual, movimiento)
                    # next_cubo.mostrar_estado()
                    self.estado_inicial.caras = sig_estado.caras
                    return self.build_solution_path(sig_estado)
                next_cubo_str = sig_estado.toString()
                if next_cubo_str not in visitados:
                    sig_estado.set_padre_y_mov_padre(estado_actual, movimiento)
                    frontier.push(sig_estado)
        return []


    def build_solution_path(self, cubo):
        path = []
        while cubo.movimiento_padre is not None:
            path.append(cubo.movimiento_padre)
            cubo = cubo.cubo_padre
        self.mostrar_solucion(list(reversed(path)))

    def mostrar_solucion(self, movimientos):
        explicaciones = {'U': 'Cara Superior horario',"U'": 'Cara Superior antihorario', 'D': 'Cara Inferior horario', "D'": 'Cara Inferior antihorario',
                         'F': 'Cara Frontal horario', "F'": 'Cara Frontal antihorario', 'B': 'Cara Posterior horario', "B'": 'Cara Posterior antihorario',
                         'L': 'Cara Izquierda horario', "L'": 'Cara Izquierda antihorario', 'R': 'Cara Derecha horario', "R'": 'Cara Derecha antihorario'}
        for i in range(len(movimientos)):
            print(f'    * PASO {i+1}: {explicaciones[movimientos[i]]} ({movimientos[i]})')

    def distancia_manhattan_centro(self, pos1, centro):
        fila1, col1, cara1 = pos1
        cara1 = CARAS[cara1]
        cara2 = CARAS[centro]
        return abs(fila1 - 1) + abs(col1 - 1) + abs(cara1 - cara2)


    def funcion_heuristica(self, cubo):
        distancia_total = 0
        ubicacion_correcta_centro = {cubo.caras['U'].piezas[1][1]: 'U', cubo.caras['L'].piezas[1][1]: 'L',
                         cubo.caras['F'].piezas[1][1]: 'F', cubo.caras['D'].piezas[1][1]: 'D',
                         cubo.caras['R'].piezas[1][1]: 'R', cubo.caras['B'].piezas[1][1]: 'B'}
        for cara in cubo.caras:
            for fila in range(3):
                for col in range(3):
                    pieza = cubo.caras[cara].piezas[fila][col]
                    pos_actual = (fila, col, cara)
                    distancia_total += self.distancia_manhattan_centro(pos_actual, ubicacion_correcta_centro[pieza])
        return distancia_total + cubo.total_piezas_diferentes_a_su_centro()

    def Astar(self,  profundidad_maxima=20):
        frontera = PriorityQueue()
        frontera.put((0, self.estado_inicial, [], 0))
        explorados = set(self.estado_inicial.toString())

        while not frontera.empty() and not self.estado_inicial.esta_resuelto():
            _, estado_actual, movimientos, _ = frontera.get()
            for movimiento in estado_actual.get_acciones():
                sig_caras = copy.deepcopy(estado_actual.caras)
                sig_estado = CuboRubik()
                sig_estado.caras = sig_caras
                sig_estado.acciones[movimiento]()
                if sig_estado.esta_resuelto():
                    self.estado_inicial.caras = sig_estado.caras
                    return self.mostrar_solucion(movimientos + [movimiento])
                estado_sig_cubo_str = sig_estado.toString()
                if estado_sig_cubo_str not in explorados:
                    explorados.add(estado_sig_cubo_str)
                    if len(movimientos) + 1 <= profundidad_maxima:
                        f = len(movimientos) + 1 + self.funcion_heuristica(sig_estado)
                        sig_estado.set_padre_y_mov_padre(estado_actual, movimiento)
                        frontera.put((f, sig_estado, movimientos + [movimiento], f))
                        # print(f"f(next_cubo) = {f}, { {movimiento} } y movimientos = {movimientos}")

        return []

    def busqueda_combinada(self, profundidad_bfs=5, profundidad_Astar=20):
        if self.estado_inicial.esta_resuelto(): return []
        explorados = set(self.estado_inicial.toString())
        frontera_bfs = Queue()
        frontera_bfs.push((self.estado_inicial, []))
        frontera_astar = PriorityQueue()
        # BFS
        for nivel in range(profundidad_bfs):
            siguiente_nivel = Queue()
            while not frontera_bfs.is_empty():
                estado_actual, movimientos = frontera_bfs.pop()
                for movimiento in estado_actual.get_acciones():
                    sig_caras = copy.deepcopy(estado_actual.caras)
                    sig_estado = CuboRubik()
                    sig_estado.caras = sig_caras
                    sig_estado.acciones[movimiento]()
                    if sig_estado.esta_resuelto():
                        self.estado_inicial.caras = sig_estado.caras
                        return self.mostrar_solucion(movimientos + [movimiento])
                    sig_estado_str = sig_estado.toString()
                    if sig_estado_str not in explorados:
                        sig_estado.set_padre_y_mov_padre(estado_actual, movimiento)
                        siguiente_nivel.push((sig_estado, movimientos + [movimiento]))
                        explorados.add(sig_estado_str)
            frontera_bfs = siguiente_nivel

        while not frontera_bfs.is_empty():
            estado_actual, movimientos = frontera_bfs.pop()
            costo = len(movimientos) + self.funcion_heuristica(estado_actual)
            frontera_astar.put((costo, estado_actual, movimientos))
        # A*
        while not frontera_astar.empty():
            _, estado_actual, movimientos = frontera_astar.get()
            for movimiento in estado_actual.get_acciones():
                sig_caras = copy.deepcopy(estado_actual.caras)
                sig_estado = CuboRubik()
                sig_estado.caras = sig_caras
                sig_estado.acciones[movimiento]()
                if sig_estado.esta_resuelto():
                    self.estado_inicial.caras = sig_estado.caras
                    return self.mostrar_solucion(movimientos + [movimiento])
                sig_estado_str = sig_estado.toString()
                if sig_estado_str not in explorados:
                    explorados.add(sig_estado_str)
                    if len(movimientos) + 1 <= profundidad_Astar:
                        sig_estado.set_padre_y_mov_padre(estado_actual, movimiento)
                        costo = len(movimientos) + 1 + self.funcion_heuristica(sig_estado)
                        frontera_astar.put((costo, sig_estado, movimientos + [movimiento]))
                        # print(f"f(next_cubo) = {costo}, { {movimiento} } y movimientos = {movimientos}")

        return []


A_ = 'antihorario'


def menu():
    cubo = CuboRubik()
    while True:
        print("MINI PROYECTO CUBO RUBIK")
        print("1. Cargar cubo rubik desde archivo")
        print("2. Mostrar cubo rubik")
        print("3. Resolver cubo rubik")
        print("4. Salir")
        opcion = input("Ingrese el número de la opción deseada: ")
        if opcion == "1":
            archivo = input("Ingrese el nombre mas la extension del archivo donde se encuentre el cubo rubik (por defecto = cubo_10_movimientos_desarmado.txt): ")
            if archivo == '':
                archivo = 'cubo_10_movimientos_desarmado.txt'
            if cubo.cargar_cubo_desde_archivo(archivo):
                print("Cargado exitosamente!")
            else:
                break
        elif opcion == "2":
            cubo.mostrar_estado()
        elif opcion == "3":
            searcher = Searcher(cubo)
            searcher.busqueda_combinada()
        elif opcion == "4":
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == '__main__':
    menu()

    # MEJOR RESULTADO
    # 10 Movimientos de desarmado y resolución funcional con algoritmo combinado
    # cubo = CuboRubik()
    # cubo.girar_cara_derecha()
    # cubo.girar_cara_frontal()
    # cubo.girar_cara_frontal()
    # cubo.girar_cara_izquierda(A_)
    # cubo.girar_cara_posterior(A_)
    # cubo.girar_cara_frontal()
    # cubo.girar_cara_izquierda()
    # cubo.girar_cara_superior(A_)
    # cubo.girar_cara_superior(A_)
    # cubo.girar_cara_derecha()
    # cubo.mostrar_estado()
    #
    # searcher = Searcher(cubo)
    # inicio = time.time()
    # searcher.busqueda_combinada()
    # fin = time.time()
    # tiempo_transcurrido = fin - inicio
    # print("Tiempo transcurrido Combinada:", tiempo_transcurrido, "segundos")
