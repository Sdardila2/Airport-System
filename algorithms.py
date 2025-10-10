import heapq
from collections import deque

class GraphAlgorithms:
    def __init__(self, graph):
        self.graph = graph
    
    def bfs(self, start):
        """BFS para encontrar componentes conexas"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            current = queue.popleft()
            for neighbor in self.graph.adjacency_list.get(current, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited
    
    def is_connected(self):
        """Determina si el grafo es conexo y encuentra componentes"""
        all_vertices = set(self.graph.get_all_vertices())
        if not all_vertices:
            return True, []
        
        components = []
        visited_global = set()
        
        for vertex in all_vertices:
            if vertex not in visited_global:
                component = self.bfs(vertex)
                components.append(component)
                visited_global.update(component)
        
        is_connected = len(components) == 1
        return is_connected, components
    
    def prim_mst(self, vertices_subset=None):
        """Algoritmo de Prim para MST"""
        if vertices_subset is None:
            vertices_subset = set(self.graph.get_all_vertices())
        
        if not vertices_subset:
            return 0, []
        
        start_vertex = next(iter(vertices_subset))
        visited = {start_vertex}
        mst_edges = []
        total_weight = 0
        
        # Priority queue: (weight, current_vertex, parent_vertex)
        edges = []
        for neighbor, weight in self.graph.adjacency_list.get(start_vertex, {}).items():
            if neighbor in vertices_subset:
                heapq.heappush(edges, (weight, start_vertex, neighbor))
        
        while edges and len(visited) < len(vertices_subset):
            weight, src, dest = heapq.heappop(edges)
            
            if dest not in visited and dest in vertices_subset:
                visited.add(dest)
                mst_edges.append((src, dest, weight))
                total_weight += weight
                
                # Add edges from the new vertex
                for neighbor, new_weight in self.graph.adjacency_list.get(dest, {}).items():
                    if neighbor not in visited and neighbor in vertices_subset:
                        heapq.heappush(edges, (new_weight, dest, neighbor))
        
        return total_weight, mst_edges
    
    def dijkstra(self, start):
        """Algoritmo de Dijkstra para caminos mínimos"""
        distances = {vertex: float('inf') for vertex in self.graph.get_all_vertices()}
        predecessors = {vertex: None for vertex in self.graph.get_all_vertices()}
        distances[start] = 0
        
        priority_queue = [(0, start)]
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            if current_distance > distances[current_vertex]:
                continue
            
            for neighbor, weight in self.graph.adjacency_list.get(current_vertex, {}).items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances, predecessors
    
    def get_shortest_path(self, start, end):
        """Reconstruye el camino mínimo entre start y end"""
        distances, predecessors = self.dijkstra(start)
        
        if distances[end] == float('inf'):
            return None, float('inf')
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        
        path.reverse()
        return path, distances[end]
    
    def get_farthest_airports(self, start, k=10):
        """Encuentra los k aeropuertos más lejanos en términos de camino mínimo"""
        distances, _ = self.dijkstra(start)
        
        # Filtrar aeropuertos alcanzables y ordenar por distancia
        reachable = [(code, dist) for code, dist in distances.items() 
                    if dist != float('inf') and code != start]
        reachable.sort(key=lambda x: x[1], reverse=True)
        
        return reachable[:k]