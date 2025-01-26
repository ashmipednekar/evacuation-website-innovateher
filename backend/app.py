from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import gridfs
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB Configuration
mongo = PyMongo(app, uri="mongodb+srv://ashmipednekar:59Dk0F56@gumpack-cluster.u6mjj.mongodb.net/buildings?retryWrites=true&w=majority&appName=gumpack-cluster")


# Use the actual database for GridFS
fs = gridfs.GridFS(mongo.cx["buildings"])

image_dir = os.path.abspath("../images/")

coordinates = {
    "WALC": [40.42745640945242, -86.91315917419448],
    "WTHR": [40.426572076226556, -86.91311613186498],
    "ME": [40.42843062305387, -86.91287552883526],
    "STEW": [40.42569297705542, -86.9128632559344],
    "RAIL": [40.42814381169848, -86.91266152817163],
    "POTR": [40.427417476606976, -86.91214638953542],
    "ELLT": [40.42818286864327, -86.91507137604114],
    "PSYC": [40.427234449585484, -86.91479352817169]
}


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
'''
floorImages = {} 
currentBuilding = os.listdir(image_dir)[0].split("_")[0]
currentMaps = []

for file in os.listdir(image_dir):
    file_path = os.path.join(image_dir, file)
    if len(file.split("_")) < 2:
        continue
    floor_number_str = file.split("_")[1].split(".")[0]
    try:
        floor_number = int(floor_number_str)  # Safely convert to integer
    except ValueError:
        continue  # Skip files that don't match the expected format
    
    with open(file_path, "rb") as image_file:
        image_id = fs.put(image_file, filename=file)
        
        # Check if building has changed
        if file.split("_")[0] != currentBuilding:
            # Store the previous building's floor images
            floorImages[currentBuilding] = currentMaps
            currentMaps = []
            currentBuilding = file.split("_")[0]

        currentMaps.append({
            "floorNumber": floor_number,
            "imageId": str(image_id)  # Store imageId as a string
        })

# Add the last building's floor images
floorImages[currentBuilding] = currentMaps

for buildingName in floorImages.keys(): 
    # Building document
    building = {
        "buildingName": f"{buildingName}",
        "floors": floorImages[buildingName],
        "minFloor": min(floor["floorNumber"] for floor in floorImages[buildingName]),
        "maxFloor": max(floor["floorNumber"] for floor in floorImages[buildingName]),
        "coords": {
            "type": "Point",
            "coordinates": coordinates[buildingName]
        }
    }

    # Insert the document into the `buildings` collection
    result = mongo.db.buildings.insert_one(building)
    print(f"Building added with ID: {result.inserted_id}")

print("Images uploaded and buildings added successfully!")
'''

# Get nearest buildings
@app.route('/buildings/near', methods=['GET'])
def get_nearest_buildings():
    user_lat = float(request.args.get('lat'))
    user_lng = float(request.args.get('lng'))
    max_distance = int(request.args.get('max_distance', 5000))  # Mock max distance

    buildings = mongo.db.buildings.find()

    for building in buildings:
            building["_id"] = str(building["_id"])
            

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