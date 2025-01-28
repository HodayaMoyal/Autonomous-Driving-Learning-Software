import os
from ultralytics import YOLO
import cv2
import geopy.distance
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from flask_cors import CORS
from flask_cors import CORS
import distance
import requests

current_lat = None
current_lng = None

# app = Flask(__name__)
# CORS(app)
# global_current_lat = None
# global_current_lng = None


def get_current_location():
  """
  This function retrieves the current latitude and longitude stored in global variables
  previously set by the updatePosition function.
  """
  # Access global variables containing current location data
  # current_lat = distance.global_current_lat
  # current_lng = distance.global_current_lng
  current_lat,current_lng = distance.update_position()

  # Check if data is available (might be None initially)
  if current_lat is None or current_lng is None:
    return None  # Indicate no data available
  else:
    return current_lat, current_lng  # Return current location as a tuple

def get_traffic_sign_center(image_path, model_path="last.pt", confidence_threshold=0.5):
  """
  Detects a traffic sign in the image using YOLO, extracts its center point (latitude and longitude),
  and returns it as a dictionary.

  Args:
      image_path (str): Path to the image file.
      model_path (str, optional): Path to the YOLO model file (default: "last.pt").
      confidence_threshold (float, optional): Confidence threshold for detections (default: 0.5).

  Returns:
      dict: Dictionary containing 'lat' and 'lng' keys for the detected traffic sign center point,
            or None if no sign is detected or conversion fails.
  """

  # Load the image
  image = cv2.imread(image_path)

  # Load the YOLO model
  model = YOLO(model_path)

  # Perform object detection
  results = model(image)[0]  # Handle potential list of results for multi-image processing

  # Initialize center point variables
  center_x, center_y = 0, 0

  # Extract center point of the first detected object (assuming only one sign)
  for result in results.boxes.data.tolist():
      x1, y1, x2, y2, score, class_id = result

      # Apply confidence threshold
      if score > confidence_threshold:
          # Calculate center point in normalized coordinates
          center_x_normalized = (x1 + x2) / (2 * image.shape[1])
          center_y_normalized = (y1 + y2) / (2 * image.shape[0])

          # Replace this with your actual function to convert normalized coordinates to lat/lng
          center_lat, center_lng = convert_normalized_to_latlng(center_x_normalized, center_y_normalized)
          print('center_lat',center_lat,'center_lng',center_lng)
          return {'lat': center_lat, 'lng': center_lng}

  # No traffic sign detected or conversion failed
  return None

def convert_normalized_to_latlng(x, y):
  """
  Converts normalized image coordinates (x, y) to latitude and longitude
  using a pre-defined mapping (replace with your actual implementation).

  Args:
      x (float): Normalized x-coordinate (between 0 and 1).
      y (float): Normalized y-coordinate (between 0 and 1).

  Returns:
      tuple: A tuple containing latitude and longitude (float, float).
  """

  # Replace with your actual logic for retrieving lat/lng based on normalized coordinates
  # This could involve a lookup table, spatial transformation function, etc.
  # Example (assuming a simple linear mapping for illustration purposes):
  image_width, image_height = 640, 640  # Replace with actual image dimensions if needed
  reference_lat, reference_lng = 31.30829, 34.61822  # Replace with known reference coordinates
  lat_range, lng_range = 0.1, 0.2  # Replace with actual latitude and longitude ranges

  latitude = reference_lat + y * (lat_range / image_height)
  longitude = reference_lng + x * (lng_range / image_width)

  return latitude, longitude

def calculate_distance_and_stop(sign_center_lat, sign_center_lng, current_lat, current_lng, current_speed, stop_threshold=1):
  """
  Calculates the distance between the detected traffic sign and the current location,
  and checks if the distance is less than a threshold to stop the vehicle (adjust stop_threshold as needed).

  Args:
      sign_center_lat (float): Latitude of the detected traffic sign center.
      sign_center_lng (float): Longitude of the detected traffic sign center.
      current_lat (float): Current latitude of the vehicle.
      current_lng (float): Current longitude of the vehicle.
      current_speed (float): Current speed of the vehicle (in angular units, replace with actual units).
      stop_threshold (float, optional): Distance threshold to stop the vehicle (meters, default: 1).

  Returns:
      dict: Dictionary containing 'distance' (meters), 'stop' (boolean), and 'new_speed' (angular units).
  """

  # Convert coordinates to Geopy objects for distance calculation
  sign_coords = (sign_center_lat, sign_center_lng)
  current_coords = (current_lat, current_lng)

  # Calculate distance using Geopy
  distance_in_meters = geopy.distance.geodesic(sign_coords, current_coords).m

  # Determine stopping decision based on distance and threshold
  stop = distance_in_meters < stop_threshold  # Change '<' to '<=' for stopping at the threshold

  # Adjust speed based on stopping decision (replace with actual speed control logic)
  new_speed = 0 if stop else current_speed  # Set new speed to zero if stopping, otherwise keep current speed

  return {'distance': distance_in_meters, 'stop': stop, 'new_speed': new_speed}








if __name__ == '__main__':
  
  
    image_path = "i.jpg"

    sign_center = get_traffic_sign_center(image_path)

#   get_current_location()
#   print('global_current_lng',current_lng)
#   print('global_current_lat',current_lat)
  
#   if current_lat is None or current_lng is None:
#     print("Failed to retrieve current location from Angular application.")
  
  
  # Example usage (assuming the function is defined above)
#   position_data = distance.update_position()  # Call the function to get lat/lng

# if position_data and position_data.get('message') == 'Position update received successfully':
#   # Access the lat and lng values from the dictionary
#   global_current_lat = position_data.get('lat')
#   global_current_lng = position_data.get('lng')

#   # Now you can use global_current_lat and global_current_lng elsewhere in your script
#   print(f"Received location: Latitude: {global_current_lat}, Longitude: {global_current_lng}")
# else:
#   print("Error receiving location data")
  
  
#   current_speed = 10  # Replace with actual current speed (in your angular units)

#   # Path to the image you want to process
#   image_path = "i.jpg"

#   # Detect traffic sign
#   sign_center = get_traffic_sign_center(image_path)

#   if sign_center:
#     sign_center_lat, sign_center_lng = sign_center['lat'], sign_center['lng']

#     # Calculate distance and stopping decision
#     distance_and_stop_result = calculate_distance_and_stop(sign_center_lat, sign_center_lng, current_lat, current_lng, current_speed)

#     print(f"Sign detected: {sign_center}")
#     print(f"Distance to sign: {distance_and_stop_result['distance']:.2f} meters")
#     print(f"Stop the vehicle: {distance_and_stop_result['stop']}")
#     print(f"New speed: {distance_and_stop_result['new_speed']}")

#     # Implement logic to control vehicle speed based on distance_and_stop_result['new_speed']
#     # (This might involve interfacing with your vehicle's control system, likely requiring additional libraries or hardware)
#   else:
#     print("No traffic sign detected in the image.")
