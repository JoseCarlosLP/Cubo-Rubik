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
        b = 2
        if sentido == 'horario':
            orden = ['U', 'L', 'D', 'R']
            a = 2
            b = 0
        temp_cara_u = self.caras[orden[0]].piezas[-1]
        self.caras[orden[0]].piezas[-1] = [fila[a] for fila in self.caras[orden[1]].piezas]
        temp_cara_lado = [fila[b] for fila in self.caras[orden[3]].piezas]
        for i in range(len(self.caras[orden[1]].piezas)):
            self.caras[orden[1]].piezas[i][a] = self.caras[orden[2]].piezas[0][i]
            self.caras[orden[3]].piezas[i][b] = temp_cara_u[i]
        self.caras[orden[2]].piezas[0] = temp_cara_lado

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
    cubo.girar_cara_frontal('horario')
    print("MOV = F")
    cubo.mostrar_estado()

    cubo.girar_cara_frontal()
    print("MOV = F'")
    cubo.mostrar_estado()
