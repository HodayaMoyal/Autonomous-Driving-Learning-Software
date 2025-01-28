import cv2


# קביעת נתיב לוידאו המקורי ולוידאו המחותך
video_path = "o.mp4"
output_path = "cut_video.mp4"

# הגדרת הזמן ממנו יתחיל החיתוך (בשניות)
start_time = 12  # לדוגמה, כאן החיתוך יתחיל מהדקה הראשונה

# פתיחת וידאו המקורי
cap = cv2.VideoCapture(video_path)

# קביעת מאפייני הוידאו (רוחב, גובה וקצב פריימים)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# יצירת אובייקט VideoWriter עבור הוידאו המחותך
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # קודקוד לפורמט MP4
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# קירוב לזמן מתחילת החיתוך בפריימים
start_frame = int(start_time * fps)

# הקפצת הוידאו לפריים המתאים
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# קריאה והקלטה של הפריימים מהוידאו המקורי ושמירתם בוידאו המחותך
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)

# סגירת וידאוים
cap.release()
out.release()

print("סיימנו לחתוך את הוידאו")
