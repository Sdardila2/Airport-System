import folium
import os

class MapVisualizer:
    def __init__(self, graph):
        self.graph = graph
    
    def plot_all_airports(self, output_file="airports_map.html"):
        """Crea un mapa con todos los aeropuertos"""
        if not self.graph.vertices:
            print("No hay aeropuertos para mostrar")
            return None
        
        # Centro del mapa en el primer aeropuerto
        first_vertex = next(iter(self.graph.vertices.values()))
        m = folium.Map(
            location=[first_vertex['lat'], first_vertex['lon']],
            zoom_start=2
        )
        
        # Añadir marcadores para cada aeropuerto
        for code, info in self.graph.vertices.items():
            folium.Marker(
                [info['lat'], info['lon']],
                popup=f"<b>{code}</b><br>{info['name']}<br>{info['city']}, {info['country']}",
                tooltip=code
            ).add_to(m)
        
        m.save(output_file)
        print(f"Mapa guardado como: {output_file}")
        return m
    
    def plot_shortest_path(self, path, output_file="shortest_path.html"):
        """Dibuja el camino mínimo en el mapa"""
        if not path:
            print("Camino vacío")
            return None
        
        # Crear mapa centrado en el primer aeropuerto del camino
        first_airport = self.graph.vertices[path[0]]
        m = folium.Map(
            location=[first_airport['lat'], first_airport['lon']],
            zoom_start=4
        )
        
        # Añadir marcadores y línea de ruta
        coordinates = []
        for i, code in enumerate(path):
            info = self.graph.vertices[code]
            coordinates.append([info['lat'], info['lon']])
            
            # Marcador especial para inicio y fin
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
        
        # Dibujar línea que conecta los aeropuertos
        folium.PolyLine(
            coordinates,
            color='blue',
            weight=3,
            opacity=0.7,
            popup="Ruta más corta"
        ).add_to(m)
        
        m.save(output_file)
        print(f"Ruta guardada como: {output_file}")
        return m