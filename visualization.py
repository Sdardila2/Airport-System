import folium

class MapVisualizer:
    def __init__(self, graph):
        self.graph = graph
    
    def plot_all_airports(self, output_file="airports_map.html"):
        if not self.graph.vertices:
            return None
        
        first_vertex = next(iter(self.graph.vertices.values()))
        m = folium.Map(location=[first_vertex['lat'], first_vertex['lon']], zoom_start=2)
        
        for code, info in self.graph.vertices.items():
            folium.Marker(
                [info['lat'], info['lon']],
                popup=f"<b>{code}</b><br>{info['name']}<br>{info['city']}, {info['country']}",
                tooltip=code
            ).add_to(m)
        
        m.save(output_file)
        return m
    
    def plot_shortest_path(self, path, output_file="shortest_path.html"):
        if not path:
            return None
        
        first_airport = self.graph.vertices[path[0]]
        m = folium.Map(location=[first_airport['lat'], first_airport['lon']], zoom_start=4)
        
        coordinates = []
        for i, code in enumerate(path):
            info = self.graph.vertices[code]
            coordinates.append([info['lat'], info['lon']])
            
            if i == 0:
                icon_color = 'green'
            elif i == len(path) - 1:
                icon_color = 'red'
            else:
                icon_color = 'blue'
            
            folium.Marker(
                [info['lat'], info['lon']],
                popup=f"<b>{code}</b><br>{info['name']}<br>{info['city']}, {info['country']}",
                tooltip=f"{i+1}. {code}",
                icon=folium.Icon(color=icon_color)
            ).add_to(m)
        
        folium.PolyLine(
            coordinates, color='blue', weight=3, opacity=0.7, popup="Ruta más corta"
        ).add_to(m)
        
        m.save(output_file)
        return m