from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

def load_map_data(filename):
    filepath = os.path.join(app.root_path, 'mapdata', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"dimensions": {"width": 2400, "height": 600}, "nodes": [], "edges": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/mapdata/<floor_id>')
def get_map_data(floor_id):
    file_map = {
        'ground': 'ablock_ground.json',
        'first': 'ablock_1.json',
        'second': 'ablock_2.json'
    }
    filename = file_map.get(floor_id, 'ablock_ground.json')
    return jsonify(load_map_data(filename))

if __name__ == '__main__':
    app.run(debug=True, port=5000)