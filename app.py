from flask import Flask, render_template, request, jsonify
import os
from graph import AirportGraph
from algorithms import GraphAlgorithms
from visualization import MapVisualizer

app = Flask(__name__)

graph = AirportGraph()
algorithms = None
visualizer = None

def initialize_data():
    global algorithms, visualizer
    csv_file = "data/flights_final.csv"
    
    if not os.path.exists(csv_file):
        return False
    
    try:
        graph.build_from_csv(csv_file)
        algorithms = GraphAlgorithms(graph)
        visualizer = MapVisualizer(graph)
        return True
    except Exception as e:
        print(f"Error initializing data: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/route')
def route():
    return render_template('route.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/api/airport/<code>')
def get_airport(code):
    if not algorithms:
        return jsonify({'success': False, 'error': 'System not initialized'})
    
    info = graph.get_vertex_info(code.upper())
    return jsonify({'success': bool(info), 'data': info})

@app.route('/api/farthest/<code>')
def get_farthest_airports(code):
    if not algorithms:
        return jsonify([])
    
    farthest = algorithms.get_farthest_airports(code.upper(), 10)
    result = [
        {
            'code': airport_code,
            'name': graph.get_vertex_info(airport_code)['name'],
            'city': graph.get_vertex_info(airport_code)['city'],
            'country': graph.get_vertex_info(airport_code)['country'],
            'distance': round(distance, 2)
        }
        for airport_code, distance in farthest
    ]
    return jsonify(result)

@app.route('/api/shortest-path')
def get_shortest_path():
    if not algorithms:
        return jsonify({'success': False, 'error': 'System not initialized'})
    
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    
    path, distance = algorithms.get_shortest_path(origin, destination)
    
    if path:
        route_details = []
        for code in path:
            info = graph.get_vertex_info(code)
            route_details.append({
                'code': code, 'name': info['name'], 'city': info['city'],
                'country': info['country'], 'lat': info['lat'], 'lon': info['lon']
            })
        
        filename = f"static/ruta_{origin}_{destination}.html"
        visualizer.plot_shortest_path(path, filename)
        
        return jsonify({
            'success': True,
            'distance': round(distance, 2),
            'path': route_details,
            'map_url': f"/{filename}"
        })
    
    return jsonify({'success': False, 'error': 'No path exists between these airports'})

@app.route('/api/graph-analysis')
def get_graph_analysis():
    if not algorithms:
        return jsonify({'error': 'System not initialized'})
    
    is_connected, components = algorithms.is_connected()
    
    mst_results = []
    total_weight = 0
    for i, comp in enumerate(components, 1):
        weight, _ = algorithms.prim_mst(comp)
        total_weight += weight
        mst_results.append({'component': i, 'vertices': len(comp), 'weight': round(weight, 2)})
    
    num_routes = sum(len(neighbors) for neighbors in graph.adjacency_list.values()) // 2
    
    return jsonify({
        'is_connected': is_connected,
        'total_components': len(components),
        'total_airports': len(graph.vertices),
        'total_routes': num_routes,
        'mst': mst_results,
        'total_mst_weight': round(total_weight, 2)
    })

@app.route('/api/generate-map')
def generate_map():
    if not visualizer:
        return jsonify({'error': 'System not initialized'})
    
    filename = "static/airports_map.html"
    visualizer.plot_all_airports(filename)
    return jsonify({'map_url': f'/{filename}'})

@app.route('/test')
def test():
    return "Initialized"

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    if initialize_data():
        print("System initialized successfully.")
    else:
        print("Error during system initialization.")
    
    print("Server running at http://localhost:5001/")
    app.run(debug=True, host='0.0.0.0', port=5001)