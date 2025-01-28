import cv2
import time

video_path = "cut_video.mp4"
cap = cv2.VideoCapture(video_path)

# Initialize variables
frame_count = 0
start_time = time.time()
fps = 0
running = True  # משתנה לבקרת הלולאה

while running and cap.isOpened():
    ret, frame = cap.read()

    if ret:
        frame_count += 1
        elapsed_time = time.time() - start_time

        if elapsed_time >= 1.0:  # Every second
            fps = frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            frame_count = 0
            start_time = time.time()

        # Display the frame (optional)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False  # יציאה מהלולאה במקרה של לחיצה על 'q'
    else:
        running = False  # יציאה מהלולאה במקרה של סוף הוידאו או שגיאה בקריאת פריים

cap.release()
cv2.destroyAllWindows()
