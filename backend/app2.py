from flask import Flask, render_template, request, redirect, url_for, jsonify
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

# Home Route
@app.route("/")
def index():
    buildings = mongo.db.buildings.find()  # Fetch buildings from MongoDB
    return render_template("index.html", buildings=buildings)


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



if __name__ == "__main__":
    app.run(debug=True)
