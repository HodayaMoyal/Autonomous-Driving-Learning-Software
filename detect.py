import torch

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt')  # Replace with your model path

# Function to perform detection
def detect_objects(image_path):
    results = model(image_path)
    # Assume the first detected object for simplicity
    first_object = results.xyxy[0][0]  # [x1, y1, x2, y2, confidence, class]
    x1, y1, x2, y2 = first_object[:4]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y
