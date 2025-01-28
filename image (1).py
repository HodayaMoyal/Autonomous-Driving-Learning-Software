import os
from ultralytics import YOLO
import cv2

def detect_objects(image_path, model_path):
    # Load the model
    model = YOLO(model_path)

    # Load the image
    image = cv2.imread(image_path)

    # Perform object detection
    results = model(image)[0]  # Handle potential list of results for multi-image processing
    
    # Draw bounding boxes and labels
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > 0.5:  # Apply a confidence threshold
            # Calculate center point
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # Print center point
            print("Center point of bounding box:", (center_x, center_y))

    # Display the image with detections
    cv2.imshow('Image with Detections', image)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

# Define image path
image_path = os.path.abspath('images\streetView2.png')

# Define model path
model_path = "last.pt"

# Call the function
detect_objects(image_path, model_path)
