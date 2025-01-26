from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock data for buildings and floor plans
mock_buildings = [
    {
        "_id": "1",
        "name": "Building A",
        "coordinates": {"type": "Point", "coordinates": [114.169, 22.319]},
        "floor_maps": ["floor1.png", "floor2.png", "floor3.png"],
    },
    {
        "_id": "2",
        "name": "Building B",
        "coordinates": {"type": "Point", "coordinates": [114.170, 22.320]},
        "floor_maps": ["floor1.png", "floor2.png"],
    },
]

# Get nearest buildings
@app.route('/buildings/near', methods=['GET'])
def get_nearest_buildings():
    user_lat = float(request.args.get('lat'))
    user_lng = float(request.args.get('lng'))
    max_distance = int(request.args.get('max_distance', 5000))  # Mock max distance

    # Simulate finding the nearest building (just return the first one for now)
    nearest_building = mock_buildings[0]
    return jsonify([nearest_building])

# Get floor plans
@app.route('/buildings/<building_id>/floorplans', methods=['GET'])
def get_floorplans(building_id):
    # Simulate getting floor plans for the specified building
    building = next((b for b in mock_buildings if b["_id"] == building_id), None)
    if not building:
        return jsonify({"error": "Building not found"}), 404

    return jsonify({"floor_maps": building["floor_maps"]})

if __name__ == '__main__':
    app.run(debug=True)