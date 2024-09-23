import math
import heapq

class Djisktra():
    from ..model.vertex import Vertex

    def __init__(self, vertices:list[Vertex]):
        from ..model.vertex import Vertex
        self.paths = {}
        self.distances = []
        self.startVertex: Vertex = None
        self.vertices = vertices


    def findPath(self, start: Vertex, adjacencyMatrix: list[list[float]]):
        self.startVertex = start
        startIndex = self.vertices.index(start)
        n = len(self.vertices)
        s = set()  # Processed vertices
        d = [math.inf] * n  # Distance array, initialize to infinity
        d[startIndex] = 0  # Distance to the start vertex is 0
        predecessors = [None] * n  # Track predecessors to reconstruct paths

        # Step 2: Initialize D array with distances from start
        for i in range(n):
            d[i] = adjacencyMatrix[startIndex][i] if i != startIndex else 0
            if adjacencyMatrix[startIndex][i] < math.inf:
                predecessors[i] = startIndex  # Direct connection to start

        s.add(startIndex)  # Step 7: Add start vertex to S

        # Repeat for all vertices
        for _ in range(n - 1):
            # Step 8: Find w in V - S such that D[w] is minimum
            w = self._minDistanceVertex(d, s)

            if w is None:
                break  # No more vertices to process

            s.add(w)  # Step 7: Add w to S

            # Step 9: For each v in V - S, update D[v]
            for v in range(n):
                if v not in s:
                    new_dist = d[w] + adjacencyMatrix[w][v]
                    if new_dist < d[v]:
                        d[v] = new_dist
                        predecessors[v] = w  # Update predecessor of v

        # Build paths from predecessors array
        self.paths = self._buildPath(predecessors, startIndex)
        self.distances = d
        return  

    def _minDistanceVertex(self, D, S):
        min_distance = math.inf
        min_vertex = None
        for i in range(len(D)):
            if i not in S and D[i] < min_distance:
                min_distance = D[i]
                min_vertex = i
        return min_vertex

    def _buildPath(self, predecessors, startIndex):
        paths = {}
        for v in range(len(predecessors)):
            path = []
            current = v
            visited = set()  # To track visited nodes

            # Backtrack from v to start_id using predecessors
            while current is not None:
                # Check for circular reference
                if current in visited:
                    break
                visited.add(current)

                path.insert(0, current)
                current = predecessors[current]

            if path and path[0] == startIndex:  # Only add the path if it starts at the source
                paths[v] = path
        return paths
    
    # def useDjisktra1(self, start: Vertex):
        # Step 1: Initialization
        distances = {vertex: math.inf for vertex in self.vertices}  # Dictionary for vertex distances
        distances[start] = 0  # Distance to the start vertex is 0
        previousVertices = {vertex: None for vertex in self.vertices}  # To store the shortest path tree

        # Min-heap priority queue, starting with the source
        priorityQueue = [(0, start)]  # (distance, vertex)

        while priorityQueue:
            currentDistance, currentVertex = heapq.heappop(priorityQueue)

            # If the popped vertex has a greater distance than the recorded distance, skip it
            if currentDistance > distances[currentVertex]:
                continue

            # Step 2: Process each neighbor of the current vertex
            currentVertexIndex = self.vertices.index(currentVertex)
            for neighborIndex, weight in enumerate(self.adjacencyMatrix[currentVertexIndex]):
                if weight == math.inf:  # Skip if there's no edge
                    continue
                
                neighborVertex = self.vertices[neighborIndex]
                distance = currentDistance + weight  # Relax the edge

                # Step 3: Relaxation
                if distance < distances[neighborVertex]:
                    distances[neighborVertex] = distance
                    previousVertices[neighborVertex] = currentVertex
                    heapq.heappush(priorityQueue, (distance, neighborVertex))

        return distances, previousVertices 
