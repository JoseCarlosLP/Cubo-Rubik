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
        # self.piezas = [[Pieza('1'),Pieza('2'),Pieza('3')],
        #                [Pieza('4'),Pieza('5'),Pieza('6')],
        #                [Pieza('7'),Pieza('8'),Pieza('9')]]

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

    def girar_cara(self, cara, sentido='horario'):
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

    def girar_cara_frontal(self, sentido='horario'):
        self.girar_cara('F', sentido)
        if sentido == 'horario':
            temp_cara_u = [fila[-1] for fila in self.caras['L'].piezas]
            temp_cara_lado = [fila[0] for fila in self.caras['R'].piezas]
            for i in range(len(self.caras['L'].piezas)):
                self.caras['L'].piezas[i][-1] = self.caras['D'].piezas[0][i]
                self.caras['R'].piezas[i][0] = self.caras['U'].piezas[-1][i]
            self.caras['D'].piezas[0] = temp_cara_lado[::-1]
            self.caras['U'].piezas[-1] = temp_cara_u[::-1]
        elif sentido == 'antihorario':
            temp_cara_u = copy.deepcopy(self.caras['U'].piezas[-1])
            self.caras['U'].piezas[-1] = [fila[0] for fila in self.caras['R'].piezas]
            temp_cara_lado = [fila[-1] for fila in self.caras['L'].piezas]
            for i in range(len(self.caras['R'].piezas)):
                self.caras['R'].piezas[i][0] = self.caras['D'].piezas[0][-(i + 1)]
                self.caras['L'].piezas[i][-1] = temp_cara_u[-(i + 1)]
            self.caras['D'].piezas[0] = temp_cara_lado

    def girar_cara_trasera(self, sentido='horario'):
        self.girar_cara('B', sentido)
        if sentido == 'horario':
            temp_cara_u = copy.deepcopy(self.caras['U'].piezas[0])
            self.caras['U'].piezas[0] = [fila[-1] for fila in self.caras['R'].piezas]
            temp_cara_lado = [fila[0] for fila in self.caras['L'].piezas]
            for i in range(len(self.caras['R'].piezas)):
                self.caras['R'].piezas[i][-1] = self.caras['D'].piezas[-1][-(i + 1)]
                self.caras['L'].piezas[i][0] = temp_cara_u[-(i + 1)]
            self.caras['D'].piezas[-1] = temp_cara_lado
        elif sentido == 'antihorario':
            temp_cara_u = [fila[0] for fila in self.caras['L'].piezas]
            temp_cara_lado = [fila[-1] for fila in self.caras['R'].piezas]
            for i in range(len(self.caras['L'].piezas)):
                self.caras['L'].piezas[i][0] = self.caras['D'].piezas[-1][i]
                self.caras['R'].piezas[i][-1] = self.caras['U'].piezas[0][i]
            self.caras['D'].piezas[-1] = temp_cara_lado[::-1]
            self.caras['U'].piezas[0] = temp_cara_u[::-1]

    def girar_cara_derecha(self, sentido='horario'):
        self.girar_cara('R', sentido)
        orden = ['B', 'U', 'F', 'D']
        if sentido == 'antihorario':
            orden = ['B', 'D', 'F', 'U']
        temp_cara = [copy.deepcopy(fila[0]) for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].set_color_a_pieza(-(i + 1), 0, self.caras[orden[1]].piezas[i][-1].get_color())
            self.caras[orden[1]].set_color_a_pieza(i, -1, self.caras[orden[2]].piezas[i][-1].get_color())
            self.caras[orden[2]].set_color_a_pieza(i, -1, self.caras[orden[3]].piezas[i][-1].get_color())
            self.caras[orden[3]].set_color_a_pieza(i, -1, temp_cara[-(i + 1)].get_color())

    def girar_cara_izquierda(self, sentido='horario'):
        self.girar_cara('L', sentido)
        orden = ['B', 'D', 'F', 'U']
        if sentido == 'antihorario':
            orden = ['B', 'U', 'F', 'D']
        temp_cara = [copy.deepcopy(fila[-1]) for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].set_color_a_pieza(-(i + 1), -1, self.caras[orden[1]].piezas[i][0].get_color())
            self.caras[orden[1]].set_color_a_pieza(i, 0, self.caras[orden[2]].piezas[i][0].get_color())
            self.caras[orden[2]].set_color_a_pieza(i, 0, self.caras[orden[3]].piezas[i][0].get_color())
            self.caras[orden[3]].set_color_a_pieza(i, 0, temp_cara[-(i + 1)].get_color())

    def girar_cara_superior(self, sentido='horario'):
        self.girar_cara('U', sentido)
        orden = ['F', 'R', 'B', 'L']
        if sentido == 'antihorario':
            orden = ['F', 'L', 'B', 'R']
        temp_cara = copy.deepcopy(self.caras[orden[0]].piezas[0])
        self.caras[orden[0]].piezas[0] = self.caras[orden[1]].piezas[0]
        self.caras[orden[1]].piezas[0] = self.caras[orden[2]].piezas[0]
        self.caras[orden[2]].piezas[0] = self.caras[orden[3]].piezas[0]
        self.caras[orden[3]].piezas[0] = temp_cara

    def girar_cara_inferior(self, sentido='horario'):
        self.girar_cara('D', sentido)
        orden = ['F', 'L', 'B', 'R']
        if sentido == 'antihorario':
            orden = ['F', 'R', 'B', 'L']
        temp_cara = copy.deepcopy(self.caras[orden[0]].piezas[-1])
        self.caras[orden[0]].piezas[-1] = self.caras[orden[1]].piezas[-1]
        self.caras[orden[1]].piezas[-1] = self.caras[orden[2]].piezas[-1]
        self.caras[orden[2]].piezas[-1] = self.caras[orden[3]].piezas[-1]
        self.caras[orden[3]].piezas[-1] = temp_cara

    def girar_cara_m(self,sentido='horario'):
        orden = ['B', 'D', 'F', 'U']
        if sentido == 'antihorario':
            orden = ['B', 'U', 'F', 'D']
        temp_cara = [copy.deepcopy(fila[1]) for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].set_color_a_pieza(-(i + 1), 1, self.caras[orden[1]].piezas[i][1].get_color())
            self.caras[orden[1]].set_color_a_pieza(i, 1, self.caras[orden[2]].piezas[i][1].get_color())
            self.caras[orden[2]].set_color_a_pieza(i, 1, self.caras[orden[3]].piezas[i][1].get_color())
            self.caras[orden[3]].set_color_a_pieza(i, 1, temp_cara[-(i + 1)].get_color())

    def girar_cara_e(self,sentido='horario'):
        orden = ['F', 'L', 'B', 'R']
        if sentido == 'antihorario':
            orden = ['F', 'R', 'B', 'L']
        temp_cara = copy.deepcopy(self.caras[orden[0]].piezas[1])
        self.caras[orden[0]].piezas[1] = self.caras[orden[1]].piezas[1]
        self.caras[orden[1]].piezas[1] = self.caras[orden[2]].piezas[1]
        self.caras[orden[2]].piezas[1] = self.caras[orden[3]].piezas[1]
        self.caras[orden[3]].piezas[1] = temp_cara

    def girar_cara_s(self, sentido='horario'):
        if sentido == 'horario':
            temp_cara_u = [fila[1] for fila in self.caras['L'].piezas]
            temp_cara_lado = [fila[1] for fila in self.caras['R'].piezas]
            for i in range(len(self.caras['L'].piezas)):
                self.caras['L'].piezas[i][1] = self.caras['D'].piezas[1][i]
                self.caras['R'].piezas[i][1] = self.caras['U'].piezas[1][i]
            self.caras['D'].piezas[1] = temp_cara_lado[::-1]
            self.caras['U'].piezas[1] = temp_cara_u[::-1]
        elif sentido == 'antihorario':
            temp_cara_u = copy.deepcopy(self.caras['U'].piezas[1])
            self.caras['U'].piezas[1] = [fila[1] for fila in self.caras['R'].piezas]
            temp_cara_lado = [fila[1] for fila in self.caras['L'].piezas]
            for i in range(len(self.caras['R'].piezas)):
                self.caras['R'].piezas[i][1] = self.caras['D'].piezas[1][-(i + 1)]
                self.caras['L'].piezas[i][1] = temp_cara_u[-(i + 1)]
            self.caras['D'].piezas[1] = temp_cara_lado



    def mostrar_estado(self):
        print("CUBO RUBIK")
        for cara in self.caras:
            print(f"Cara {cara}:")
            for fila in self.caras[cara].piezas:
                print(" ".join([c.color for c in fila]))
            print()

    def pruebas(self):
        #for _ in range(5):
        self.girar_cara_trasera()
        self.girar_cara_inferior()
        self.girar_cara_superior()
        self.girar_cara_inferior()
        self.girar_cara_superior()
        self.girar_cara_derecha()
        self.girar_cara_derecha()
        self.girar_cara_trasera('antihorario')
        self.girar_cara_superior()
        self.girar_cara_superior()
        self.girar_cara_frontal()
        self.girar_cara_izquierda('antihorario')
        self.girar_cara_izquierda('antihorario')


if __name__ == '__main__':
    cubo = CuboRubik()
    cubo.pruebas()
    cubo.mostrar_estado()

    cubo.girar_cara_s('antihorario')
    cubo.mostrar_estado()
