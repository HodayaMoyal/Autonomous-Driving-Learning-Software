from packeges import *

def convert_normalized_to_latlng(x, y, reference_lat, reference_lng):
    image_width, image_height = 640, 640  
    lat_range, lng_range = 0.1, 0.2  

    latitude = reference_lat + y * (lat_range / image_height)
    longitude = reference_lng + x * (lng_range / image_width)

    return latitude, longitude

def convert_meters_to_latlng(meters_x, meters_y, reference_lat, reference_lng):
    # 1 degree latitude is approximately 111,320 meters
    # 1 degree longitude is approximately 111,320 * cos(latitude) meters
    lat_per_meter = 1 / 111320
    lng_per_meter = 1 / (111320 * np.cos(np.radians(reference_lat)))

    latitude = reference_lat + (meters_y * lat_per_meter)
    longitude = reference_lng + (meters_x * lng_per_meter)

    return latitude, longitude

def initialize_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None
    return cap

def process_frame(frame, model, initial_lat, initial_lng, threshold):
    H, W, _ = frame.shape
    results = model(frame)[0]

    # Center of the frame (driver's point)
    center_x, center_y = W // 2, H // 2
    center_x_normalized = center_x / W
    center_y_normalized = center_y / H
    driver_lat, driver_lng = convert_normalized_to_latlng(center_x_normalized, center_y_normalized, initial_lat, initial_lng)
    print(f"Driver's Point: (Lat: {driver_lat:.6f}, Lng: {driver_lng:.6f})")

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Calculate the object's center point
            object_center_x = (x1 + x2) / 2
            object_center_y = (y1 + y2) / 2
            object_center_x_normalized = object_center_x / W
            object_center_y_normalized = object_center_y / H
            object_lat, object_lng = convert_normalized_to_latlng(object_center_x_normalized, object_center_y_normalized, initial_lat, initial_lng)

            print(f"Object's Point: (Lat: {object_lat:.6f}, Lng: {object_lng:.6f})")
            print(f"Detected {results.names[int(class_id)]} with score {score:.2f}")

            # Calculate distance between object and driver
            object_point = (object_lat, object_lng)
            driver_point = (driver_lat, driver_lng)
            distance_km = geodesic(object_point, driver_point).kilometers
            print(f"Distance to {results.names[int(class_id)]}: {distance_km:.2f} km")

            # Display distance on the frame
            distance_text = f"Distance to {results.names[int(class_id)]}: {distance_km:.2f} km"
            cv2.putText(frame, distance_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            color = (0, 255, 0)  # Green color for demonstration
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)

    cv2.imshow('Real-time Detection', frame)
    return frame

def process_video(video_path, model_path, initial_lat, initial_lng, speed_m_per_s, threshold):
    cap = initialize_video(video_path)
    if cap is None:
        return

    model = YOLO(model_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = 0
    start_time = time.time()
    fps_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            return

        frame_count += 1 
        elapsed_time = time.time() - start_time

        if elapsed_time >= 1.0:  # Every second
            fps = fps_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            fps_count = 0
            start_time = time.time()
        fps_count += 1

        elapsed_time_seconds = frame_count / fps
        distance_travelled = elapsed_time_seconds * speed_m_per_s
        meters_x = distance_travelled
        meters_y = 0  # No movement along the y-axis (northward)

        current_lat, current_lng = convert_meters_to_latlng(meters_x, meters_y, initial_lat, initial_lng)

        frame = process_frame(frame, model, initial_lat, initial_lng, threshold)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    cap.release()
    cv2.destroyAllWindows()

# Main function to run the video processing
def main():
    video_path = 'video/cut_video.mp4'
    model_path = "last.pt"
    initial_lat = 31.30829
    initial_lng = 34.61822
    speed_m_per_s = 10  
    threshold = 0.5

    process_video(video_path, model_path, initial_lat, initial_lng, speed_m_per_s, threshold)

if __name__ == "__main__":
    main()