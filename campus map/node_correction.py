from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

MAPDATA_DIR = os.path.join(app.root_path, 'mapdata')
STATIC_DIR = os.path.join(app.root_path, 'static')

@app.route('/')
def index():
    return render_template('node_correction.html')

# API: Automatically discover all available floor map files
@app.route('/api/available-floors')
def get_available_floors():
    json_files = []
    svg_files = []

    if os.path.exists(MAPDATA_DIR):
        json_files = [f for f in os.listdir(MAPDATA_DIR) if f.endswith('.json')]
    
    if os.path.exists(STATIC_DIR):
        svg_files = [f for f in os.listdir(STATIC_DIR) if f.endswith('.svg')]

    # Pair JSON files with matching SVG files
    floors = []
    for j_file in sorted(json_files):
        base_name = os.path.splitext(j_file)[0]
        
        # Try to find matching SVG (e.g., ablock_ground.json -> ablock_ground.svg or ablock_first.svg)
        matching_svg = None
        for s_file in svg_files:
            s_base = os.path.splitext(s_file)[0]
            if base_name in s_base or s_base in base_name:
                matching_svg = s_file
                break

        floors.append({
            'id': base_name,
            'json_file': j_file,
            'svg_file': matching_svg or (svg_files[0] if svg_files else '')
        })

    return jsonify({
        'floors': floors,
        'all_json_files': json_files,
        'all_svg_files': svg_files
    })

# API: Load specific JSON map data
@app.route('/api/mapdata/<filename>')
def get_map_file(filename):
    if not filename.endswith('.json'):
        filename += '.json'
    
    filepath = os.path.join(MAPDATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
            
    return jsonify({'error': f'File {filename} not found'}), 404

# API: Save updated JSON map data directly to disk
@app.route('/api/save-mapdata/<filename>', methods=['POST'])
def save_map_file(filename):
    if not filename.endswith('.json'):
        filename += '.json'
        
    filepath = os.path.join(MAPDATA_DIR, filename)
    try:
        data = request.get_json()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return jsonify({'success': True, 'message': f'Saved {filename} successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Node Correction Tool running on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)