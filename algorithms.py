import heapq
from collections import deque

class GraphAlgorithms:
    def __init__(self, graph):
        self.graph = graph
    
    def bfs(self, start):
        visited = {start}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            for neighbor in self.graph.adjacency_list.get(current, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited
    
    def is_connected(self):
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
        
        return len(components) == 1, components
    
    def prim_mst(self, vertices_subset=None):
        if vertices_subset is None:
            vertices_subset = set(self.graph.get_all_vertices())
        
        if not vertices_subset:
            return 0, []
        
        start_vertex = next(iter(vertices_subset))
        visited = {start_vertex}
        mst_edges = []
        total_weight = 0
        
        edges = []
        for neighbor, weight in self.graph.adjacency_list.get(start_vertex, {}).items():
            if neighbor in vertices_subset:
                heapq.heappush(edges, (weight, start_vertex, neighbor))
        
        while edges and len(visited) < len(vertices_subset):
            weight, src, dest = heapq.heappop(edges)
            
            if dest in vertices_subset and dest not in visited:
                visited.add(dest)
                mst_edges.append((src, dest, weight))
                total_weight += weight
                
                for neighbor, new_weight in self.graph.adjacency_list.get(dest, {}).items():
                    if neighbor in vertices_subset and neighbor not in visited:
                        heapq.heappush(edges, (new_weight, dest, neighbor))
        
        return total_weight, mst_edges
    
    def dijkstra(self, start):
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
        distances, _ = self.dijkstra(start)
        
        reachable = [(code, dist) for code, dist in distances.items() 
                     if dist != float('inf') and code != start]
        
        reachable.sort(key=lambda x: x[1], reverse=True)
        
        return reachable[:k]