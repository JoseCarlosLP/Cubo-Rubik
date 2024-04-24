## 1. Nombre Completo 
    Jose Carlos Lozada Peralta
## 2. Descripción
    En este proyecto se ha implementado distintos algoritmos de busqueda en espacio de estados en el tan conocido Cubo Rubik, el cual es un desafío interesante, dada la inmensa cantidad de estados posibles que tiene este cubo y los recursos computacionales limitados que tenemos, y hallar soluciones óptimas a cualquier estado.
## 3. Requerimientos del entorno de programación
    - Python, en su version más actualizada de preferencia
    - Librerias como queue y copy
## 4. Manual de uso
4.1. Formato de codificación para cargar el estado de un cubo desde el archivo de texto

    Se sugiere, para evitar problemas al momento de la ejecucion del algoritmo de solución, mantener la siguiente estructura de los centros segun la cara del cubo:
        - Cara Superior U = White 'W'
        - Cara Inferior D = Yellow 'Y'
        - Cara Izquierda L = Orange 'O'
        - Cara Frontal F = Green 'G'
        - Cara Derecha R = Red 'R'
        - Cara Posterior B = Blue 'B'

    
    W O O   |
    B W W   |   Cada 3 filas hacen una cara del cubo, empezando por la cara superior U
    B R R   |
    G O O   }
    G Y Y   }   Cara inferior D
    R R R   }
    G O O   |
    Y O O   |   Cara izquierda L
    Y W W   |
    W G G   }
    W G G   }   Cara frontal F
    R G G   }
    Y R B   |
    Y R W   |   Cara derecha R
    Y R W   |
    Y Y O   }
    B B B   }   Cara posterior B
    B B B   }

    Los caracteres | y } solo son indicadores para agrupar y mostrar las caras, no son parte de la estrucutra necesaria para cargar el cubo, simplemente se necesitan 3 columnas de los colores separadas por un espacio.


4.2. Instrucciones para ejecutar el programa

    El programa cuenta con un menu mostrando 3 opciones posibles, la primera para cargar el estado del cubo rubik desde un archivo de texto,desde la consola se puede ingresar el nombre mas la extension del archivo.
    Una vez cargado el cubo rubik en el programa, la segunda opcion te permite visualizar las 6 caras del cubo para 
    corroborar que se cargó correctamente.
    La tercera ejecuta la función encargada para resolver el cubo rubik cargado anteriormente.
    La última opción termina el programa.
## 5. Diseño e implementación
5.1. Breve descripcion de modelo del problema

    Para modelar el cubo rubik, se ha implementado un diccionario de objetos, dichos objetos son Caras, que cada cara tiene una matriz 3x3, representando las 9 piezas que tiene cada cara, esta implementacion permite acceder a cada una de las caras del cubo mediante una clave, la letra que representa cada una de las caras del cubo (U,D,B,F,R,L), a diferencia de una lista de matrices, que se manejaría por indices, lo cual puede hacer menos legible el código pero según algunas investigaciones mias, puedes que sea ligeramente más eficiente el acceso a los valores que mi implementación
5.2. Explicacion y justificacion de algoritmo(s), tecnicas, heuristicas seleccionadas

    - Como justificacion del algoritmo utilizado, escogí combinar la eficiencia de la búsqueda en amplitud, en el caso de mi computadora, realizó una búsqueda eficiente y rápida hasta el 5to nivel, imaginandonos un arbol de decisión de 12 ramas cada nodo, reprensentando las 12 acciones disponibles y posibles a partir de cada estado. Ya a partir del 6to nivel, mi BFS demoraba entre 2 o 3 minutos, lo cual podria seguir siendo considerable, pero preferí limitarlo a 5 para intentar obtener soluciunes optimas y rápidas. Una vez analizada esta  situación, se me ocurrió que a partir de los estados visitados en el 5to nivel de mis BFS, en el cual obviamente no está la solución, guardar estos estados y aplicarles la heuristica combinada que tengo programada, con el objetivo de que apartir de la búsqueda exhaustiva que se realizó hasta el 5to nivel, esos estados ya explorados, sean en el punto de partida del algoritmo A*, y con el cálculo de la heuristica a cada estado del último nivel visitado con BFS, nos estaríamos asegurando de estar más cerca de la solución que si empezaramos de 0 con A*, es por eso que decidí combinar esos 2 algoritmos, con BFS, una búsqueda exhaustiva y eficiente hasta el 5to nivel, y del 6to nivel en adelante, una búsqueda informada y más eficiente en recursos computacionales que BFS.
    
    - Las heuristicas utilizadas fueron las vistas en clases pero en otro contexto, la distancia manhattan y la cantidad de colores de piezas que no coinciden con el color del centro de la cara, osea, que no estan en su cara, esta última heurísitca no tiene mucho misterio, pero la primera un poco sí, ya que yo implementé la distancia manhattan de una pieza a la cara con el centro que corresponde a su color por que si aplicamos la distancia manhattan tal cual como se conoce, tendríamos que hallar la distancia a la que está la pieza de su posición correcta, pero acá tenemos un problema, ya que cargando un cubo rubik desarmado desde un archivo, suponiendo que la pieza W se encuentre en la cara B en la posicion [0,0], imaginandonos una matriz 3x3, y su cara correcta para esta pieza sea la cara U, por que el centro en esa cara es igual W, no podemos asumir con total certeza que la posicion correcta es la [0,0] en la cara U, por que esta pieza al estar en una esquina, su posicion correcta puede ser cualquiera de las cuatro esquinas posibles de la cara U, lo mismo sucede para las piezas que no están en las esquinas, nunca sabemos la posicion correcta exacta de una pieza hasta que lo armamos. Intenté implementar una forma en la cual no se pierda la posición correcta exacta de una pieza, pero solo funcionaba si se usaba para desarmar los giros implementados, si cargamos un cubo desde un archivo de texto, tendriamos que de igual forma cargar la posicion exacta correcta a la cual la pieza pertenece.

    - Un aspecto más que me gustaría comentar, es que implementé una manera de que no se generen ciclos de un cubo a otro, ya que si empezamos en un estado X, y damos un giro frontal horario, y de este último estado damos un giro frontal antihorario, estamos regresando al estado X inicial, entonces yo controlo que si el movimiento padre, osea el giro que te puso en tu estado actual es F, retiro de sus posibles acciones el movimiento contrario F', para así aumentar, ligeramente talvez, pero evitar tener que iterar sobre esa accion posible, ya que igual implementé un set() que igual controla los estados repetidos.

5.3. En caso de usar modelos lingüísticos, incluir los prompts clave

    - Utilicé modelos linguisticos como apoyo en funciones repetitivas, como ser la distancia manhattan, la función para leer desde un archivo el cubo, y aunque no me dieron el código exacto que necesitaba, me fué más fácil la implementación ya que me ahorro un poco de tiempo. No tengo los prompts guardados por que lastimosamente, el modelo linguistico que más llegue a utilizar y que mejores respuestas me ofreció fue Claude, el cuál resulta que no guarda el historial de las conversaciones. Y para finalizar, para obtener la estructura del algoritmo A* y mi busqueda combinada, que a pesar de que tenía la idea clara, me fué más sencillo redactarla y pedir el código al modelo de lenguaje que ponerme a implementarla de 0, que como dije anteriormente, en el 99% de los casos, solo me dieron la estructura del código, y yo tuve que ajustarlo mejor a mis necesidades.
    - Casos como el try de mi función de leer el cubo desde un archivo, si me ayudé con un modelo de lenguaje, así como la uso de funciones lambda en el atributo de acciones de mi objeto Cubo Rubik, lo cual era necesario más que todo para las funciones que reciben el parametro "antihorario", ya que era obligatorio colocar los paréntesis para colocar ese parámetro, si no, no hubiera sido necesario el uso de las funciones lambdas. Así evitamos que como la propiedad acciones esta en el constructor, esos métodos se ejecutaban al crear un objeto, pero con la función lambda, controlamos eso


## 6. Trabajo Fututo
6.1. Lista de tareas inconclusas y/o ideas para continuar con el proyecto

    - Lograr que resuelva todo tipo de cubos en un tiempo adecuado al hardware de mi computadora, no solamente algunos estados sencillos/intermedios de un cubo desarmado, o quizas mi mejor resultado, que es un cubo desarmado con 10 giros resuelto en los mismos 10 giros de manera eficiente, como un cubo medianamente complicado
    - Durante la investigacion que hice vi que se puede implementar deep learning para resolver el cubo, me interesaría intentarlo 
    - Una implementacion con numpy haría que el código se viera de menos complejidad, sobre todo al hacer los giros y seleccionar las columnas, pero me imagino que por debajo esta libería igual tiene que iterar sobre las filas y seleccionar de cada una de ellas la columna
    - Me gustaría conocer la o las heurísticas que harían que el proceso de solucion del cubo junto con el algoritmo A* aplique a más casos.
    - Por último, estaría interesante y desafiante, un solucionador genérico, para cubos de NxN.

