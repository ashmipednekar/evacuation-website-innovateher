from flask import Flask, render_template, request, redirect, url_for, jsonify
from collections.abc import MutableMapping
from flask_pymongo import PyMongo
import gridfs

app = Flask(__name__)

# MongoDB Configuration
#my pass: 59Dk0F56
app.config["MONGO_URI"] = "mongodb+srv://ashmipednekar:59Dk0F56@gumpack-cluster.u6mjj.mongodb.net/?retryWrites=true&w=majority&appName=gumpack-cluster"
mongo = PyMongo(app)

# Home Route
@app.route("/")
def index():
    buildings = mongo.db.buildings.find()  # Fetch buildings from MongoDB
    return render_template("index.html", buildings=buildings)

# Add Building
@app.route("/add", methods=["POST"])
def add_building():
    building_name = request.form.get("name")
    address = request.form.get("address")
    floors = request.form.get("floors")

    if building_name and address and floors:
        mongo.db.buildings.insert_one({
            "name": building_name,
            "address": address,
            "floors": int(floors)
        })
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
