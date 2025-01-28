import os
from ultralytics import YOLO
import cv2
import geopy.distance
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/updatePosition', methods=['POST'])

#return each second the current LAT LNG from the angular
def update_position():
  """
  Receives a POST request from the Angular application containing the current latitude and longitude.
  """
  try:
    # Access data from the request body (assuming it's sent as JSON)
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    # Validate latitude and longitude values
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
      return jsonify({'error': 'Invalid latitude or longitude'}), 400

    # Perform actions based on latitude and longitude
    # For example, you can print them for now
    print(f"Received position update - Latitude: {lat}, Longitude: {lng}")

    # You can replace the print statement with your desired logic here,
    # such as updating a database, triggering other functionalities, etc.

    return jsonify({'message': 'Position update received successfully'})

  except (KeyError, TypeError) as e:
    # Handle potential errors in accessing data from the request
    print(f"Error processing request: {e}")
    return jsonify({'error': 'Error receiving position data'}), 400



# def check_distance_and_speed(current_lat, current_lng, sign_center_x, sign_center_y, sign_type):
#     # Calculate distance between current location and sign center
#     current_location = (current_lat, current_lng)
#     sign_center = (sign_center_x, sign_center_y)
#     distance = geopy.distance.geodesic(current_location, sign_center).meters

#     # Check if sign is a stop sign and distance is less than 1 meter
#     if sign_type == 'stop_sign' and distance < 1:
#         return 0  # Assume speed is 0
#     else:
#         return None  # Speed not affected by sign


    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
  

