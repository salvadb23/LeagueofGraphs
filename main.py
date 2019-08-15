import json
from sys import argv


class Vertex(object):

    def __init__(self, vertex):
        """initialize a vertex and its neighbors
        neighbors: set of vertices adjacent to self,
        stored in a dictionary with key = vertex,
        value = weight of edge between self and neighbor.
        """
        self.id = vertex
        self.neighbors = {}

    def addNeighbor(self, vertex, weight=0):
        """add a neighbor along a weighted edge"""
        if (vertex not in self.neighbors):
            self.neighbors[vertex] = weight
    
    def getNeighborsId(self):
        """return the neighbors of this vertex"""
        return [neighbor.getId() for neighbor in self.neighbors.keys()]

    def __str__(self):
        """output the list of neighbors of this vertex"""
        return str(self.id) + " adjancent to " + str([x.id for x in self.neighbors])

    def getNeighbors(self):
        """return the neighbors of this vertex"""
        return self.neighbors

    def getId(self):
        """return the id of this vertex"""
        return self.id

    def getEdgeWeight(self, vertex):
        """return the weight of this edge"""
        return self.neighbors[vertex]


class Graph:
    def __init__(self):
        """ initializes a graph object with an empty dictionary.
        """
        self.vertList = {}
        self.numVertices = 0

    def __str__(self):
        for item in self.vertList:
            print(item)
        return 'done'

    def addVertex(self, key):
        """add a new vertex object to the graph with
        the given key and return the vertex
        """
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex

        return newVertex

    def getVertex(self, vertex):
        """return the vertex if it exists"""
        return self.vertList[vertex] if self.vertList[vertex] is not None else False

    def addEdge(self, vertexOne, vertexTwo, cost=0):
        """add an edge from vertex f to vertex t with a cost
        """
        if self.vertList[vertexOne] is None:
            self.addVertex(vertexOne)
        elif self.vertList[vertexTwo] is None:
            self.addVertex(vertexTwo)
        else:
            self.vertList[vertexOne].addNeighbor(
                self.vertList[vertexTwo], cost)

    def getVertices(self):
        """return all the vertices in the graph"""
        return self.vertList.keys()

    def find_shortest_path(self, vertex_one, vertex_two):
        '''Finds the shortest path between two vertices'''
        queue = [(vertex_one, 0)]
        visited = {}
        path = []
        while queue:
            if vertex_two in visited:
                break
            vertex, parent = queue.pop(0)
            if len(visited.keys()) is len(self.vertList):
                break
            if vertex not in visited:
                visited[vertex] = parent

            for neighbor in self.vertList[vertex].neighbors:
                if neighbor not in visited:
                    queue.append((neighbor.getId(), vertex))

        child = vertex_two
        while vertex_one not in path:
            path.append(child)
            child = visited[child]
        return path[::-1]

    def DFS_recursive(self,v,v2):
        """searches the graph to see if there is a path between two vertices using DFS"""
        vertexObj = self.vertList[v]
        visited = {}
        visited[vertexObj.getId()] = 0
        path = []

        def dfs(vertex, parent = 0):
            if parent == 0:
                visited[vertex.getId()] = parent
            if parent is not 0:
                visited[vertex.getId()] = parent.getId()
            for neighbor in vertex.neighbors:
                if neighbor.getId() not in visited:
                    dfs(neighbor, vertex)
        dfs(vertexObj)
        child = v2
        while v not in path:
            path.append(child)
            child = visited[child]

        return path[::-1]

    def clique(self, vertex):
        vertices = self.getVertices()
        clique = set([vertex])
        for v in vertices:
            vertex = self.vertList[v]
            neighbors = set(vertex.getNeighborsId())
            if clique.issubset(neighbors):
                clique.add(v)
        return clique


    def __iter__(self):
        """iterate over the vertex objects in the
        graph, to use sytax: for v in g
        """
        return iter(self.vertList.values())

g = Graph()

with open('champions.json') as champions:
    data = json.load(champions)
    counter = 0
    arr = []
    for champion in data['data']:
        if champion not in g.getVertices():
            g.addVertex(champion)
        for comparison in data['data']:
            if comparison not in g.getVertices():
                g.addVertex(comparison)
            if data['data'][champion]['tags'][0] == data['data'][comparison]['tags'][0] and champion is not comparison:
                g.addEdge(champion,comparison, 1)
            if len(data['data'][champion]['tags']) == 2 and len(data['data'][comparison]['tags']) == 2:
                if data['data'][champion]['tags'][0] == data['data'][comparison]['tags'][1]:
                    g.addEdge(champion,comparison, 2)
                if data['data'][champion]['tags'][1] == data['data'][comparison]['tags'][1]:
                    g.addEdge(champion,comparison, 2)

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def handle_input(champ1,champ2):
    nl = '\n'
    reccommended = g.clique(champ1)
    short = g.find_shortest_path(champ1, champ2)
    intersect = intersection(g.getVertex(champ1).getNeighborsId(), g.getVertex(champ2).getNeighborsId())
    print(f"{nl}")
    print(f"If you like playing {champ1} you might also like playing: {nl}{reccommended}")
    print(f"{nl}")
    print(f"The best learning path to go from {champ1} to {champ2} is {short}")
    print(f"{nl}")
    print(f"Champions similar to {champ1} and {champ2} are {intersect}")
    print(f"{nl}")
    return "GLHF!"

# print(g.getVertex('Syndra').getNeighborsId())
# print(g.clique('Xayah'))

print(handle_input(argv[1], argv[2]))