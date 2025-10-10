from flask import Flask, render_template, request, jsonify
import os
from graph import AirportGraph
from algorithms import GraphAlgorithms
from visualization import MapVisualizer

app = Flask(__name__)

# Inicializar el grafo global (igual que en la versión consola)
graph = AirportGraph()
algorithms = None
visualizer = None

def initialize_data():
    """Cargar datos al iniciar la aplicación"""
    global algorithms, visualizer
    
    csv_file = "data/flights_final.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Error: No se encuentra el archivo {csv_file}")
        return False
    
    try:
        print("🔄 Cargando datos del dataset...")
        graph.build_from_csv(csv_file)
        algorithms = GraphAlgorithms(graph)
        visualizer = MapVisualizer(graph)
        print(f"✅ Datos cargados: {len(graph.vertices)} aeropuertos")
        return True
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        return False

# Cargar datos al iniciar
initialize_data()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

# API Endpoints (simples y funcionales)
@app.route('/api/airport/<code>')
def get_airport(code):
    """Obtener información de un aeropuerto"""
    info = graph.get_vertex_info(code.upper())
    return jsonify({'success': bool(info), 'data': info})

@app.route('/api/farthest/<code>')
def get_farthest_airports(code):
    """Obtener los 10 aeropuertos más lejanos"""
    if not algorithms:
        return jsonify([])
    
    farthest = algorithms.get_farthest_airports(code.upper(), 10)
    result = []
    for airport_code, distance in farthest:
        info = graph.get_vertex_info(airport_code)
        result.append({
            'code': airport_code,
            'name': info['name'],
            'city': info['city'],
            'country': info['country'],
            'distance': round(distance, 2)
        })
    return jsonify(result)

@app.route('/api/shortest-path')
def get_shortest_path():
    """Calcular la ruta más corta entre dos aeropuertos"""
    if not algorithms:
        return jsonify({'success': False, 'error': 'Sistema no inicializado'})
    
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    
    path, distance = algorithms.get_shortest_path(origin, destination)
    
    if path:
        route_details = []
        for code in path:
            info = graph.get_vertex_info(code)
            route_details.append({
                'code': code,
                'name': info['name'],
                'city': info['city'],
                'country': info['country'],
                'lat': info['lat'],
                'lon': info['lon']
            })
        
        # Generar mapa de la ruta
        filename = f"static/ruta_{origin}_{destination}.html"
        visualizer.plot_shortest_path(path, filename)
        
        return jsonify({
            'success': True,
            'distance': round(distance, 2),
            'path': route_details,
            'map_url': f"/{filename}"
        })
    
    return jsonify({'success': False, 'error': 'No existe ruta entre los aeropuertos'})

@app.route('/api/graph-analysis')
def get_graph_analysis():
    """Obtener análisis del grafo"""
    if not algorithms:
        return jsonify({'error': 'Sistema no inicializado'})
    
    is_connected, components = algorithms.is_connected()
    
    # Calcular MST
    mst_results = []
    total_weight = 0
    for i, comp in enumerate(components, 1):
        weight, edges = algorithms.prim_mst(comp)
        total_weight += weight
        mst_results.append({
            'component': i,
            'vertices': len(comp),
            'weight': round(weight, 2)
        })
    
    return jsonify({
        'is_connected': is_connected,
        'total_components': len(components),
        'total_airports': len(graph.vertices),
        'total_routes': sum(len(neighbors) for neighbors in graph.adjacency_list.values()) // 2,
        'mst': mst_results,
        'total_mst_weight': round(total_weight, 2)
    })

@app.route('/api/generate-map')
def generate_map():
    """Generar mapa general de aeropuertos"""
    if not visualizer:
        return jsonify({'error': 'Sistema no inicializado'})
    
    filename = "static/airports_map.html"
    visualizer.plot_all_airports(filename)
    return jsonify({'map_url': f'/{filename}'})

if __name__ == '__main__':
    # Crear directorio static si no existe
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Servidor Flask iniciado")
    print("📧 URL: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)