import copy


class Pieza:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_color(self, c):
        self.color = c


class Cara:
    def __init__(self, color):
        self.piezas = [[Pieza(color) for _ in range(3)] for _ in range(3)]

    def set_color_a_pieza(self, i, j, c):
        self.piezas[i][j].set_color(c)


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

    def girar_cara_actual(self, cara, sentido='horario'):
        a = 2
        b = 0
        if sentido == 'antihorario':
            a = 0
            b = 2
        esquinas = [[0, 0], [a, b], [2, 2], [b, a]]
        centros = [[0, 1], [1, b], [2, 1], [1, a]]
        tmp_esquina = copy.deepcopy(self.caras[cara].piezas[esquinas[0][0]][esquinas[0][1]])
        tmp_centro = copy.deepcopy(self.caras[cara].piezas[centros[0][0]][centros[0][1]])
        for i in range(3):
            self.caras[cara].set_color_a_pieza(esquinas[i][0], esquinas[i][1],
                                               self.caras[cara].piezas[esquinas[i + 1][0]][
                                                   esquinas[i + 1][1]].get_color())
            self.caras[cara].set_color_a_pieza(centros[i][0], centros[i][1], self.caras[cara].piezas[centros[i + 1][0]][
                centros[i + 1][1]].get_color())

        self.caras[cara].set_color_a_pieza(esquinas[3][0], esquinas[3][1], tmp_esquina.get_color())
        self.caras[cara].set_color_a_pieza(centros[3][0], centros[3][1], tmp_centro.get_color())

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
            temp_cara_u = copy.deepcopy(self.caras['U'].piezas[a])
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
        temp_cara = [copy.deepcopy(fila[b]) for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].set_color_a_pieza(-(i + 1), b, self.caras[orden[1]].piezas[i][a].get_color())
            self.caras[orden[1]].set_color_a_pieza(i, a, self.caras[orden[2]].piezas[i][a].get_color())
            self.caras[orden[2]].set_color_a_pieza(i, a, self.caras[orden[3]].piezas[i][a].get_color())
            self.caras[orden[3]].set_color_a_pieza(i, a, temp_cara[-(i + 1)].get_color())

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
        temp_cara = copy.deepcopy(self.caras[orden[0]].piezas[a])
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
                print(" ".join([c.color for c in fila]))
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


if __name__ == '__main__':
    cubo = CuboRubik()
    cubo.pruebas()
    cubo.mostrar_estado()

    cubo.girar_cara_s()
    cubo.mostrar_estado()
