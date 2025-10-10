import pandas as pd
from haversine import haversine

class AirportGraph:
    def __init__(self):
        self.vertices = {}  # {code: {name, city, country, lat, lon}}
        self.adjacency_list = {}  # {code: {neighbor_code: distance}}
    
    def add_vertex(self, code, name, city, country, lat, lon):
        """Añade un aeropuerto al grafo"""
        self.vertices[code] = {
            'name': name,
            'city': city,
            'country': country,
            'lat': lat,
            'lon': lon
        }
        if code not in self.adjacency_list:
            self.adjacency_list[code] = {}
    
    def add_edge(self, code1, code2, distance):
        """Añade una arista no dirigida entre dos aeropuertos"""
        if code1 in self.adjacency_list and code2 in self.adjacency_list:
            self.adjacency_list[code1][code2] = distance
            self.adjacency_list[code2][code1] = distance
    
    def build_from_csv(self, file_path):
        """Construye el grafo desde un archivo CSV"""
        print("Leyendo archivo CSV...")
        df = pd.read_csv(file_path)
        
        # Primero añadir todos los vértices
        print("Añadiendo aeropuertos al grafo...")
        for _, row in df.iterrows():
            # Aeropuerto origen
            self.add_vertex(
                row['Source Airport Code'],
                row['Source Airport Name'],
                row['Source Airport City'],
                row['Source Airport Country'],
                row['Source Airport Latitude'],
                row['Source Airport Longitude']
            )
            # Aeropuerto destino
            self.add_vertex(
                row['Destination Airport Code'],
                row['Destination Airport Name'],
                row['Destination Airport City'],
                row['Destination Airport Country'],
                row['Destination Airport Latitude'],
                row['Destination Airport Longitude']
            )
        
        # Luego añadir las aristas
        print("Calculando distancias y creando rutas...")
        for _, row in df.iterrows():
            src_code = row['Source Airport Code']
            dest_code = row['Destination Airport Code']
            
            src_lat = row['Source Airport Latitude']
            src_lon = row['Source Airport Longitude']
            dest_lat = row['Destination Airport Latitude']
            dest_lon = row['Destination Airport Longitude']
            
            distance = haversine(src_lat, src_lon, dest_lat, dest_lon)
            self.add_edge(src_code, dest_code, distance)
        
        print(f"Grafo construido: {len(self.vertices)} aeropuertos")
    
    def get_vertex_info(self, code):
        """Retorna la información de un aeropuerto"""
        if code in self.vertices:
            return self.vertices[code]
        return None
    
    def get_all_vertices(self):
        """Retorna todos los códigos de aeropuertos"""
        return list(self.vertices.keys())