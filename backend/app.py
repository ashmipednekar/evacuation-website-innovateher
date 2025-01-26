from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import gridfs
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB Configuration
#my pass: 59Dk0F56
app.config["MONGO_URI"] = "mongodb+srv://ashmipednekar:59Dk0F56@gumpack-cluster.u6mjj.mongodb.net/?retryWrites=true&w=majority&appName=gumpack-cluster"
mongo = PyMongo(app)

fs = gridfs.GridFS(mongo.db)

image_dir = os.path.abspath("../images/")

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

# Upload Images
@app.route("/upload-images", methods=["POST"])
def upload_image():
    floorImages = {} 
    currentBuilding = os.listdir(image_dir)[0].split("_")[0]
    currentMaps = []
    
    for file in os.listdir(image_dir):
        file_path = os.path.join(image_dir, file)
        with open(file_path, "rb") as image_file:
            image_id = fs.put(image_file, filename=file)

            if (file.split("_")[0] != currentBuilding):
                floorImages[currentBuilding] = currentMaps
                currentMaps = []
                currentBuilding = file.split("_")[0]


            currentMaps.append({
                "floorNumber": int(file.split("_")[1]),
                "imageId": str(image_id)  # Store imageId as a string
                })
    
    for buildingName in floorImages.keys(): 
        # Building document
        building = {
            "buildingName": f"{buildingName}",
            "floors": floorImages[buildingName], # object containing floorNum and imageId
            "minFloor": min(floor["floorNumber"] for floor in floorImages[buildingName]),
            "maxFloor": max(floor["floorNumber"] for floor in floorImages[buildingName]),
            "coords": {
                "type": "Point",
                "coordinates": [-73.935242, 40.73061]  
            }
        }

        # Insert the document into the `buildings` collection

        result = mongo.db.buildings.insert_one(building)
        print(f"Building added with ID: {result.inserted_id}")

    return jsonify({"message": "Images uploaded and buildings added successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)