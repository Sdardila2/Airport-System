import pandas as pd
from haversine import haversine

class AirportGraph:
    def __init__(self):
        self.vertices = {}
        self.adjacency_list = {}
    
    def add_vertex(self, code, name, city, country, lat, lon):
        if code not in self.vertices:
            self.vertices[code] = {
                'name': name, 'city': city, 'country': country, 'lat': lat, 'lon': lon
            }
            self.adjacency_list[code] = {}
    
    def add_edge(self, code1, code2, distance):
        if code1 in self.adjacency_list and code2 in self.adjacency_list:
            self.adjacency_list[code1][code2] = distance
            self.adjacency_list[code2][code1] = distance
    
    def build_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        
        for _, row in df.iterrows():
            self.add_vertex(
                row['Source Airport Code'], row['Source Airport Name'],
                row['Source Airport City'], row['Source Airport Country'],
                row['Source Airport Latitude'], row['Source Airport Longitude']
            )
            self.add_vertex(
                row['Destination Airport Code'], row['Destination Airport Name'],
                row['Destination Airport City'], row['Destination Airport Country'],
                row['Destination Airport Latitude'], row['Destination Airport Longitude']
            )

        for _, row in df.iterrows():
            src_code = row['Source Airport Code']
            dest_code = row['Destination Airport Code']
            
            distance = haversine(
                row['Source Airport Latitude'], row['Source Airport Longitude'],
                row['Destination Airport Latitude'], row['Destination Airport Longitude']
            )
            self.add_edge(src_code, dest_code, distance)
    
    def get_vertex_info(self, code):
        return self.vertices.get(code)
    
    def get_all_vertices(self):
        return list(self.vertices.keys())