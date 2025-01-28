from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import torch
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt')  # Replace with your model path

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

lat_lng_data = {'lat': None, 'lng': None}
object_position = {'lat': None, 'lng': None}

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371
    return r * c

def detect_objects(image_path):
    results = model(image_path)
    first_object = results.xyxy[0][0]
    x1, y1, x2, y2 = first_object[:4]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x.item(), center_y.item()

@app.route('/uploadImage', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        center_x, center_y = detect_objects(file_path)
        # Use center_x, center_y to calculate distance or any other logic
        print(f"Object detected at: ({center_x}, {center_y})")

        # Assuming these coordinates need to be converted to lat/lng or some other distance calculation
        # Replace with your actual logic to convert image coordinates to lat/lng or calculate distance

        return jsonify({'center_x': center_x, 'center_y': center_y})

@app.route('/updatePosition', methods=['POST'])
def update_position():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')

        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Invalid latitude or longitude'}), 400

        lat_lng_data['lat'] = lat
        lat_lng_data['lng'] = lng

        print(f"Received position update - Latitude: {lat}, Longitude: {lng}")

        if object_position['lat'] is not None and object_position['lng'] is not None:
            distance = haversine(lat, lng, object_position['lat'], object_position['lng'])
            print(f"Distance to object: {distance} km")

        return jsonify({'message': 'Position update received successfully'})

    except (KeyError, TypeError) as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Error receiving position data'}), 400

@app.route('/setObjectPosition', methods=['POST'])
def set_object_position():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')

        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Invalid latitude or longitude'}), 400

        object_position['lat'] = lat
        object_position['lng'] = lng

        print(f"Received object position - Latitude: {lat}, Longitude: {lng}")

        return jsonify({'message': 'Object position update received successfully'})

    except (KeyError, TypeError) as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Error receiving object position data'}), 400

@app.route('/getLatLong', methods=['GET'])
def get_lat_long():
    lat = lat_lng_data['lat']
    lng = lat_lng_data['lng']
    return jsonify({'lat': lat, 'lng': lng})

@app.route('/calculateDistance', methods=['POST'])
def calculate_distance():
    try:
        data = request.get_json()
        sign_lat = data.get('sign_lat')
        sign_lng = data.get('sign_lng')

        if not (-90 <= sign_lat <= 90) or not (-180 <= sign_lng <= 180):
            return jsonify({'error': 'Invalid latitude or longitude'}), 400

        user_lat = lat_lng_data['lat']
        user_lng = lat_lng_data['lng']

        if user_lat is None or user_lng is None:
            return jsonify({'error': 'User position not available'}), 400

        distance = haversine(user_lat, user_lng, sign_lat, sign_lng)
        print(distance)
        return jsonify({'distance_km': distance})

    except (KeyError, TypeError) as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Error calculating distance'}), 400

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
