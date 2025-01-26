from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import gridfs
from bson import ObjectId
import os
import geopy.distance

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

@app.route('/buildings/<building_name>/floorplans', methods=['GET'])
def get_floorplans(building_name):
    building = mongo.db.buildings.find_one({"buildingName": building_name})

    if not building:
        return jsonify({"error": "Building not found"}), 404

    floor_plans = [floor["imageId"] for floor in building["floors"]]
    return jsonify({"floor_maps": floor_plans})

@app.route('/floorplans/<image_id>', methods=['GET'])
def get_floorplan_image(image_id):
    try:
        # Fetch the image from GridFS using the image_id
        image_data = fs.get(ObjectId(image_id))
        # Return the image as a response
        return image_data.read(), 200, {'Content-Type': 'image/jpeg'}  # Assuming images are JPEG
    except Exception as e:
        # Handle errors (e.g., invalid ObjectId or missing image)
        return jsonify({"error": "Image not found"}), 404

# Get nearest buildings
@app.route('/buildings/near', methods=['GET'])
def get_nearest_buildings():
    user_lat = float(request.args.get('lat'))
    user_lng = float(request.args.get('lng'))
    user_coords = (user_lat, user_lng)
    min_distance = float('inf')  # Start with a very high value
    nearest_building = None

    buildings = mongo.db.buildings.find()  # Fetch all buildings

    for building in buildings:
        # Extract building coordinates
        build_lng = building["coords"]["coordinates"][0]
        build_lat = building["coords"]["coordinates"][1]
        build_coords = (build_lat, build_lng)

        # Calculate distance
        distance = geopy.distance.geodesic(user_coords, build_coords).km
        if distance < min_distance:
            min_distance = distance
            nearest_building = building

    if nearest_building:
        # Serialize nearest building (convert ObjectId to string)
        nearest_building["_id"] = str(nearest_building["_id"])
        return jsonify(nearest_building)
    else:
        # If no buildings are found
        return jsonify({"error": "No nearby buildings found"}), 404





if __name__ == '__main__':
    app.run(debug=True)