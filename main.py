class Pieza:
    def __init__(self, color):
        self.color = color


class Cara:
    def __init__(self, color):
        self.piezas = [[Pieza(color) for _ in range(3)] for _ in range(3)]


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

    def girar_cara_frontal(self, sentido='antihorario'):
        orden = ['U', 'R', 'D', 'L']
        a = 0
        b = -1
        if sentido == 'horario':
            orden = ['U', 'L', 'D', 'R']
            a = -1
            b = 0
        temp_cara_u = self.caras[orden[0]].piezas[-1]
        self.caras[orden[0]].piezas[-1] = [fila[a] for fila in self.caras[orden[1]].piezas]
        temp_cara_lado = [fila[b] for fila in self.caras[orden[3]].piezas]
        for i in range(len(self.caras[orden[1]].piezas)):
            self.caras[orden[1]].piezas[i][a] = self.caras[orden[2]].piezas[0][i]
            self.caras[orden[3]].piezas[i][b] = temp_cara_u[i]
        self.caras[orden[2]].piezas[0] = temp_cara_lado

    def girar_cara_trasera(self, sentido='antihorario'):
        orden = ['U', 'L', 'D', 'R']
        a = 0
        b = -1
        if sentido == 'horario':
            orden = ['U', 'R', 'D', 'L']
            a = -1
            b = 0
        temp_cara_u = self.caras[orden[0]].piezas[0]
        self.caras[orden[0]].piezas[0] = [fila[a] for fila in self.caras[orden[1]].piezas]
        temp_cara_lado = [fila[b] for fila in self.caras[orden[3]].piezas]
        for i in range(len(self.caras[orden[1]].piezas)):
            self.caras[orden[1]].piezas[i][a] = self.caras[orden[2]].piezas[-1][i]
            self.caras[orden[3]].piezas[i][b] = temp_cara_u[i]
        self.caras[orden[2]].piezas[-1] = temp_cara_lado

    def girar_cara_derecha(self, sentido='antihorario'):
        orden = ['D', 'F', 'U', 'B']
        if sentido == 'horario':
            orden = ['U', 'F', 'D', 'B']
        temp_cara = [fila[-1] for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].piezas[i][-1] = self.caras[orden[1]].piezas[i][-1]
            self.caras[orden[1]].piezas[i][-1] = self.caras[orden[2]].piezas[i][-1]
            self.caras[orden[2]].piezas[i][-1] = self.caras[orden[3]].piezas[i][0]
            self.caras[orden[3]].piezas[i][0] = temp_cara[i]

    def girar_cara_izquierda(self, sentido='antihorario'):
        orden = ['U', 'F', 'D', 'B']
        if sentido == 'horario':
            orden = ['D', 'F', 'U', 'B']
        temp_cara = [fila[0] for fila in self.caras[orden[0]].piezas]
        for i in range(len(temp_cara)):
            self.caras[orden[0]].piezas[i][0] = self.caras[orden[1]].piezas[i][0]
            self.caras[orden[1]].piezas[i][0] = self.caras[orden[2]].piezas[i][0]
            self.caras[orden[2]].piezas[i][0] = self.caras[orden[3]].piezas[i][-1]
            self.caras[orden[3]].piezas[i][-1] = temp_cara[i]

    def girar_cara_superior(self, sentido='antihorario'):
        orden = ['F', 'L', 'B', 'R']
        if sentido == 'horario':
            orden = ['F', 'R', 'B', 'L']
        temp_cara = self.caras[orden[0]].piezas[0]
        self.caras[orden[0]].piezas[0] = self.caras[orden[1]].piezas[0]
        self.caras[orden[1]].piezas[0] = self.caras[orden[2]].piezas[0]
        self.caras[orden[2]].piezas[0] = self.caras[orden[3]].piezas[0]
        self.caras[orden[3]].piezas[0] = temp_cara

    def girar_cara_inferior(self, sentido='antihorario'):
        orden = ['F', 'R', 'B', 'L']
        if sentido == 'horario':
            orden = ['F', 'L', 'B', 'R']
        temp_cara = self.caras[orden[0]].piezas[-1]
        self.caras[orden[0]].piezas[-1] = self.caras[orden[1]].piezas[-1]
        self.caras[orden[1]].piezas[-1] = self.caras[orden[2]].piezas[-1]
        self.caras[orden[2]].piezas[-1] = self.caras[orden[3]].piezas[-1]
        self.caras[orden[3]].piezas[-1] = temp_cara

    def mostrar_estado(self):
        for cara in self.caras:
            print(f"Cara {cara}:")
            for fila in self.caras[cara].piezas:
                print(" ".join([c.color for c in fila]))
            print()


if __name__ == '__main__':
    cubo = CuboRubik()
    print('ESTADO INICIAL')
    cubo.mostrar_estado()

    # cubo.girar_cara_frontal('horario')
    # print("MOV = F")
    # cubo.mostrar_estado()
    #
    # cubo.girar_cara_frontal()
    # print("MOV = F'")
    # cubo.mostrar_estado()

    # print("MOV = R'")
    # cubo.girar_cara_derecha()
    # cubo.mostrar_estado()
    # print('MOV = R')
    # cubo.girar_cara_derecha('horario')
    # cubo.mostrar_estado()

    # print('MOV = L')
    # cubo.girar_cara_izquierda('horario')
    # cubo.mostrar_estado()
    # print("MOV = L'")
    # cubo.girar_cara_izquierda()
    # cubo.mostrar_estado

    # print("MOV = B'")
    # cubo.girar_cara_trasera()
    # cubo.mostrar_estado()
    # print('MOV = B')
    # cubo.girar_cara_trasera('horario')
    # cubo.mostrar_estado()

    # print('MOV = U')
    # cubo.girar_cara_superior('horario')
    # cubo.mostrar_estado()
    # print("MOV = U'")
    # cubo.girar_cara_superior()
    # cubo.mostrar_estado()

    print('MOV = D')
    cubo.girar_cara_inferior('horario')
    cubo.mostrar_estado()
    print("MOV = D'")
    cubo.girar_cara_inferior()
    cubo.mostrar_estado()

