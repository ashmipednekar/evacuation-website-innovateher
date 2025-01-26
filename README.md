
# Fire Evacuation Hub

## Prerequisites

### Frontend Dependencies
- Node.js (v14+ recommended)
- npm or yarn

### Backend Dependencies
- Python 3.8+
- pip

## Installation

### Frontend Setup
1. Install dependencies:
```bash
npm install axios react react-dom google-maps-react
```

### Backend Setup
1. Install Python dependencies:
```bash
pip install flask flask-cors flask-pymongo gridfs geopy.distance bson
```

### Environment Configuration
- Create `.env` file with:
  - MongoDB connection string
  - Google Maps API key

## Running the Project

### Frontend
```bash
cd frontend
npm start
```

### Backend
```bash
cd backend
python app.py
```
