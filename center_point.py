from packeges import *
# import yaml

# Load data.yaml to get the names of the classes
# with open('data.yaml', 'r') as f:
#     data = yaml.safe_load(f)
# class_names = data['names']

def take_screenshot():
    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    # Convert the screenshot to a numpy array
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return image

def save_image(image, folder_name, filename):
    # Ensure the directory exists
    os.makedirs(folder_name, exist_ok=True)
    # Generate file path
    image_path = os.path.join(folder_name, filename)
    # Save the image to the specified file path
    cv2.imwrite(image_path, image)
    return image_path

def draw_circle_around_sign(image, x1, y1, x2, y2, output_path):
    # Calculate the center point
    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)
    # Calculate the radius as half the width of the bounding box
    radius = int((x2 - x1) / 2)
    # Draw the circle on the image
    cv2.circle(image, (center_x, center_y), radius, (0, 0, 255), 2)
    # Save the image with the circle
    cv2.imwrite(output_path, image)
    
def crop_image_borders(image, top, bottom, left, right):
    height, width, _ = image.shape
    cropped_image = image[top:height-bottom, left:width-right]
    return cropped_image

def get_traffic_sign_center(model_path="last.pt", confidence_threshold=0.5):
    class_name = ""
    # Take a screenshot
    screenshot_image = take_screenshot()
    # Crop the borders of the image
    top, bottom, left, right = 100, 100, 100, 100  # Adjust these values as needed
    cropped_image = crop_image_borders(screenshot_image, top, bottom, left, right)
    # Save the cropped image to the screenshot directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    cropped_image_path = save_image(cropped_image, 'screenshot', f'cropped_screenshot_{timestamp}.png')
    # Load the YOLO model
    model = YOLO(model_path)
    # Perform object detection
    results = model(cropped_image)[0]  # Handle potential list of results for multi-image processing
    detected = False
    center_lat, center_lng = None, None
    # Extract center point of each detected object
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        # Apply confidence threshold
        if score > confidence_threshold:
            detected = True
            # Adjust coordinates for the cropped image
            x1 += left
            y1 += top
            x2 += left
            y2 += top
            # Debug: print coordinates and score
            print(f"Detection: x1={x1}, y1={y1}, x2={x2}, y2={y2}, score={score}")
            # Calculate center point in normalized coordinates
            center_x_normalized = (x1 + x2) / (2 * screenshot_image.shape[1])
            center_y_normalized = (y1 + y2) / (2 * screenshot_image.shape[0])
            # Convert normalized coordinates to lat/lng
            center_lat, center_lng = convert_normalized_to_latlng(center_x_normalized, center_y_normalized)
            # Draw circle around the detected traffic sign immediately
            output_image_path = os.path.join('screenshot', f'detected_sign_{timestamp}.png')
            draw_circle_around_sign(screenshot_image, x1, y1, x2, y2, output_image_path)
            # Optionally, print or save results
            # class_name = class_names[int(class_id)]  # Convert class_id to int
            print(f"Detected sign at LAT: {center_lat}, LNG: {center_lng}")
    return {'lat': center_lat, 'lng': center_lng, 'class_name': class_name} if detected else None

def convert_normalized_to_latlng(x, y):
    image_width, image_height = 640, 640
    reference_lat, reference_lng = 31.30829, 34.61822
    lat_range, lng_range = 0.1, 0.2
    latitude = reference_lat + y * (lat_range / image_height)
    longitude = reference_lng + x * (lng_range / image_width)
    return latitude, longitude
