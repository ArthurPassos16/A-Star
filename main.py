# Implementando um Algoritmo A* para Resolução de Labirintos
# Arthur Passos, Eduarda Chagas e Gabriel Sousa
# Link do youtube: https://youtu.be/tYSYfbRMIRs
# 
# Imports necessários
import math
import queue

# Limites do ambiente
bound_x = 15
bound_y = 15

#####################################################################################
#
# Classe Point
# Representa um ponto no espaço euclidiano, onde x representa o eixo vertical e y o eixo horizontal
#
#####################################################################################
class Point:
    # Inicialização de um ponto
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # Distância euclidiana para outro ponto
    def euclidian_distance_to(self, other):
        return math.sqrt(
            math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    # Distância manhattan para outro ponto
    def manhattan_distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    # Verifica se o ponto é válido
    def is_valid(self):
        return self.x >= 0 and self.x < bound_x and self.y >= 0 and self.y < bound_y

    # Verifica se dois pontos são iguais
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Retorna a soma entre dois pontos (x1+x2, y1+y2)
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # Retorna o hash de um objeto do tipo ponto
    def __hash__(self):
        return hash((self.x, self.y))

    # Retorna a string que representa o ponto
    def __str__(self):
        return f"({self.x}, {self.y})"


# Vetor de movimento que representa todas as possibilidades de movimento
movement_vector = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, 1),
    Point(0, -1),
    Point(-1, 1),
    Point(-1, -1),
    Point(1, 1),
    Point(1, -1)
]


#####################################################################################
#
# Classe Cell
# Representa uma célula no ambiente, podendo ser livre ou bloqueada
#
#####################################################################################
class Cell:
    def __init__(self,
                 point: Point,
                 value: int,
                 parent=None,
                 f=math.inf,
                 g=math.inf,
                 h=math.inf):
        self.point = point
        self.parent = parent
        self.value = value
        self.f = f
        self.g = g
        self.h = h

    # Calcula a função heurística para um destino
    def heuristic_to(self, dest, heuristic="euclidian"):
        if heuristic == "euclidian":
            self.h = self.point.euclidian_distance_to(dest.point)
        elif heuristic == "manhattan":
            self.h = self.point.manhattan_distance_to(dest.point)

    # Verifica se a célula contém o ponto passado em other
    def is_same(self, other: Point):
        return other.x == self.point.x and other.y == self.point.y

    # Retorna a string que representa a célula
    def __str__(self):
        return f"({self.point.x}, {self.point.y})"

    # Verifica se duas células são as mesmas células
    def __eq__(self, other):
        return self.point.x == other.point.x and self.point.y == other.point.y

    # Verifica se a célula é maior que a célula other
    def __gt__(self, other):
        return self.f > other.f

    # Verifica se a célula é menor que a célula other
    def __st__(self, other):
        return self.f < other.f

    def backtrack_to_source(self, backtrack_list=[]):
        if self.parent:
            backtrack_list.append(self)
            return self.parent.backtrack_to_source(backtrack_list)
        backtrack_list.append(self)
        return backtrack_list


# Retorna uma lista que possui o menor caminho do ponto source para o ponto dest, utilizando o algoritmo A*
def a_star(grid, source, dest, heuristic):
    # Teste de validação
    if (not (source.is_valid() and dest.is_valid())):
        print("Pontos inválidos")
        return -1
    if (source == dest):
        print("Já está no destino.")
        return -2
    if (grid[source] == 1 or grid[dest] == 1):
        print("Início ou destino bloqueados(valores igual a 1)")
        return -3

    # Inicializa as células de início e fim
    start_cell = Cell(source, grid[source])
    start_cell.g = start_cell.h = start_cell.f = 0
    end_cell = Cell(dest, grid[dest])
    end_cell.g = end_cell.h = end_cell.f = 0

    # Inicializa a fila de prioridade
    fronteira = queue.PriorityQueue()
    # Inicializa uma lista dos pontos que ainda não foram explorados
    explorados = {}

    fronteira.put(start_cell)

    while (not fronteira.empty()):
        # Passa para current_node o primeiro elemento da fila(O elemento que possui o menor valor f(x))
        current_node = fronteira.get()
        explorados[Point(current_node.point.x,
                         current_node.point.y)] = current_node

        # Verificar se o current_node é o destino
        if (current_node.is_same(dest)):
            # Retorna o menor caminho de source para dest
            return current_node.backtrack_to_source()

        for i in range(len(movement_vector)):
            # Calcula a posição do ponto filho
            child_point = Point(current_node.point.x,
                                current_node.point.y) + movement_vector[i]
            if child_point.is_valid():
                # Verifica se o ponto filho é desbloqueado
                if grid[child_point] == 1:
                    continue

                # Cria um filho do tipo cell a partir do ponto
                child = Cell(child_point, grid[child_point])
                child.parent = current_node

                # Verifica se o ponto a ser explorado já foi explorado
                if child.point in explorados.keys():
                    continue

                # g(x)
                child.g = current_node.g + (1 if current_node.value == 0 else math.inf)
                # h(X)
                child.heuristic_to(end_cell, heuristic)
                # f(x) = g(x) + h(x)
                child.f = child.g + child.h

                fronteira.put(child)
    return 0


grid = {}

f = open('input1.txt', 'r')
lines = f.readlines()
i = 0
j = 0


for line in lines:
    j = 0
    numbers = line.split(' ')
    for number in numbers:
        number = number.replace('\n', '')
        if (number != ''):
            grid[Point(i, j)] = int(number)
        j += 1
    i += 1

backtrack_list = a_star(grid, Point(0, 1), Point(14, 13), 'euclidian')
if type(backtrack_list) == type([]):
    backtrack_list.reverse()
    for item in backtrack_list:
        grid[item.point] = 'X'
        print(item, end=" -> ")
print()
print("Mapa resolvido: ")
for i in range(bound_x):
    for j in range(bound_y):
        print(grid[Point(i, j)], end=" ")
    print()

if (backtrack_list == 0):
    print("Nao foi possivel achar um caminho.")
