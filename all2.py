import requests

def get_current_location():
  """
  Fetches the current latitude and longitude from the Flask app.
  """
  # Replace with the actual URL of your Flask app's updatePosition endpoint
  url = "http://localhost:5000/updatePosition"

  try:
    response = requests.post(url, json={})  # Send an empty JSON body (optional)
    response.raise_for_status()  # Raise an exception for unsuccessful responses

    # Extract data from the response (assuming it's JSON)
    data = response.json()
    if data.get('message') == 'Position update received successfully':
      return data.get('lat'), data.get('lng')
    else:
      print("Error retrieving location data from server")
      return None, None  # Indicate error or missing data

  except requests.exceptions.RequestException as e:
    print(f"Error fetching location data: {e}")
    return None, None  # Indicate error

# ... (rest of your code using get_current_location())
if __name__ == '__main__':

    current_lat, current_lng = get_current_location()
    print(current_lat,current_lng)
# Now you can use current_lat and current_lng in your logic

