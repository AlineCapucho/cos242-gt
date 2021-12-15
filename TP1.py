from collections import deque
from queue import Queue, LifoQueue
import copy

#### Actual Code ####

class Graph:
    def __init__(self):
        # Initially, just initialize the deque and does nothing more
        self.vertices = deque()
        self.matrix = deque()
        self.kind = ''
        self.graus = deque()

    def create(self, v, e, kind='list'):
        # This function must create the graph
        if kind == 'list':
            self.kind = 'list'
            for i in range(1, v+1):
                self.graus.append(0)
                self.vertices.append(Vertice(i))
            
            for u, v in e:
                self.vertices[u-1].vizinhos.append(v)
                self.graus[u-1] += 1

                self.vertices[v-1].vizinhos.append(u)
                self.graus[v-1] += 1
        elif kind == 'matrix':
            self.kind = 'matrix'

            for i in range(v):
                self.graus.append(0)
                self.matrix.append(deque(0 for j in range(v)))

            for u, v in e:
                self.matrix[u-1][v-1] = 1
                self.graus[u-1] += 1

                self.matrix[v-1][u-1] = 1
                self.graus[v-1] += 1
        else:
            raise Exception('Invalid kind.')
    
    def create_from_file(self, filename, kind='list'):
        # This function must create a graph by reading a file
        with open(filename, 'r') as f:
            ver = int(f.readline())
            if kind == 'list':
                self.kind = 'list'
                for i in range(1, ver+1):
                    self.graus.append(0)
                    self.vertices.append(Vertice(i))
                
                for line in f.readlines():
                    u = int(line[0])
                    v = int(line[2])

                    self.vertices[u-1].vizinhos.append(v)
                    self.graus[u-1] += 1

                    self.vertices[v-1].vizinhos.append(u)
                    self.graus[u-1] += 1
            elif kind == 'matrix':
                self.kind = 'matrix'
                for i in range(ver):
                    self.graus.append(0)
                    self.matrix.append(deque(0 for j in range(ver)))
                
                for line in f.readlines():
                    u = int(line[0])
                    v = int(line[2])

                    self.matrix[u-1][v-1] = 1
                    self.graus[u-1] += 1

                    self.matrix[v-1][u-1] = 1
                    self.graus[v-1] += 1
            else:
                raise Exception('Invalid kind.')
    
    def __repr__(self):
        # Creates a print representation to visualize the contents
        if self.kind == 'list':
            vertices = 'number of vertices: {}'.format(str(len(self.vertices)))
            edges = ''

            for v in self.vertices:
                edges += "edges of vertice {}: ".format(str(v.id))
                edges += ''.join('{}, '.format(str(edge)) if edge != v.vizinhos[-1] else \
                    str(edge) for edge in v.vizinhos)
                edges += '\n'
            
            return vertices + '\n' + edges
        elif self.kind == 'matrix':
            vertices = 'number of vertices: {}'.format(str(len(self.matrix[0])))
            edges = ''

            for i, u in enumerate(self.matrix):
                edges += "edges of vertice {}: ".format(str(i+1))

                for j, v in enumerate(u):
                    if v:
                        edges += "{}, ".format(str(j+1))
                edges = edges.rstrip(', ')
                edges += "\n"

            return vertices + '\n' + edges
        else:
            raise Exception('This graph was not initialized')

    def search(self, b):
        self.__bfs__(b)
        self.__dfs__(b)

    def __bfs__(self, b):
        if self.kind == 'list':
            self.bfsMarks = []
            self.bfsExplored = []
            self.bfsPai = []
            self.bfsNivel = []
            self.bfsQueue = Queue()

            for i in range(len(self.vertices)):
                self.bfsMarks.append(0)
                self.bfsPai.append(0)
                self.bfsNivel.append(0)
            self.bfsMarks[b-1] = 1
            self.bfsQueue.put(b)

            while(self.bfsQueue.empty() != True):
                v = self.bfsQueue.get()
                vizinhos = self.vertices[v-1].vizinhos

                for i in range (len(vizinhos)):
                    if self.bfsMarks[vizinhos[i]-1] == 0:
                        self.bfsMarks[vizinhos[i]-1] = 1
                        self.bfsQueue.put(vizinhos[i])
                        self.bfsPai[vizinhos[i]-1] = v
                        self.bfsNivel[vizinhos[i] - 1] = self.bfsNivel[self.bfsPai[vizinhos[i] - 1] - 1] + 1
                self.bfsExplored.append(v)

            # ordem dos vertices explorados
            # vetor dos vertices pais: self.bfsPai[0] = 2 quer dizer que o vertice 2 eh o pai do vertice 1
            # vetor do nivel dos vertices na arvore geradora, [0] corresponde ao vertice 1, etc. o nivel da origem eh 0
            # print(self.bfsExplored) 
            # print(self.bfsPai)
            # print(self.bfsNivel)

        elif self.kind == 'matrix':
            self.bfsMarks = []
            self.bfsExplored = []
            self.bfsPai = []
            self.bfsNivel = []
            self.bfsQueue = Queue()

            for i in range(len(self.matrix[0])):
                self.bfsMarks.append(0)
                self.bfsPai.append(0)
                self.bfsNivel.append(0)
            self.bfsMarks[b-1] = 1
            self.bfsQueue.put(b)

            while(self.bfsQueue.empty() != True):
                v = self.bfsQueue.get()
                for i in range(len(self.matrix[0])):
                    if self.matrix[v-1][i] == 1:
                        if self.bfsMarks[i] == 0:
                            self.bfsMarks[i] = 1
                            self.bfsQueue.put(i+1)
                            self.bfsPai[i] = v
                            self.bfsNivel[i] = self.bfsNivel[self.bfsPai[i] - 1] + 1
                self.bfsExplored.append(v)
            
            # print(self.bfsExplored)
            # print(self.bfsPai)
            # print(self.bfsNivel)

        else:
            raise Exception('Invalid kind.')

    def __dfs__(self, b):
        if self.kind == 'list':
            self.dfsMarks = []
            self.dfsExplored = []
            self.dfsPai = []
            self.dfsNivel = []
            self.dfsStack = LifoQueue()

            for i in range(len(self.vertices)):
                self.dfsMarks.append(0)
                self.dfsPai.append(0)
                self.dfsNivel.append(0)
        
            self.dfsStack.put(b)

            while(self.dfsStack.empty() != True):
                v = self.dfsStack.get()
                vizinhos = self.vertices[v-1].vizinhos
                if(self.dfsMarks[v-1] == 0):
                    self.dfsMarks[v-1] = 1
                    self.dfsExplored.append(v)
                    for i in range (len(vizinhos)-1, -1, -1):
                        self.dfsStack.put(vizinhos[i])
                        if(self.dfsMarks[vizinhos[i]-1] == 0):
                            self.dfsPai[vizinhos[i]-1] = v
                            self.dfsNivel[vizinhos[i] - 1] = self.dfsNivel[self.dfsPai[vizinhos[i] - 1] - 1] + 1

            # print(self.dfsExplored)
            # print(self.dfsPai)
            # print(self.dfsNivel)

        elif self.kind == 'matrix':
            self.dfsMarks = []
            self.dfsExplored = []
            self.dfsPai = []
            self.dfsNivel = []
            self.dfsStack = LifoQueue()

            for i in range(len(self.matrix[0])):
                self.dfsMarks.append(0)
                self.dfsPai.append(0)
                self.dfsNivel.append(0)

            self.dfsStack.put(b)

            while(self.dfsStack.empty() != True):
                v = self.dfsStack.get()
                if(self.dfsMarks[v-1] == 0):
                    self.dfsMarks[v-1] = 1
                    self.dfsExplored.append(v)
                    for i in range(len(self.matrix[0])-1, -1, -1):
                        if self.matrix[v-1][i] == 1:
                            self.dfsStack.put(i+1)
                            if(self.dfsMarks[i] == 0):
                                self.dfsPai[i] = v
                                self.dfsNivel[i] = self.dfsNivel[self.dfsPai[i] - 1] + 1

            # print(self.dfsExplored)
            # print(self.dfsPai)
            # print(self.dfsNivel)

        else:
            raise Exception('Invalid kind.')

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()
        self.nivel = 0

#### Testing ####

""" Testing the create function """
# vertices = [1, 2, 3, 4, 5, 6, 7, 8]
# edges = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 8), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]

# mygraph = Graph()
# mygraph.create(8, edges, kind='list')
# # print(mygraph)

# mygraph.search(1)

""" Testing the create_from_file function """
mygraph = Graph()
mygraph.create_from_file('test2.txt', kind='list')
# print(mygraph)
mygraph.search(1)

mygraph2 = Graph()
mygraph2.create_from_file('test2.txt', kind='matrix')
# print(mygraph)
mygraph2.search(1)


#### TAIL ####