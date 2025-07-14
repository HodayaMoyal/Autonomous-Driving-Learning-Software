🧠 Autonomous Driving Learning Software
A Full-Stack System for Real-Time Traffic Sign Recognition, Visualization, and Driver Compliance Validation

🔍 Overview
This project is an intelligent simulation and validation platform designed to teach and demonstrate autonomous driving capabilities, with a primary focus on traffic sign recognition and compliance. The system detects and classifies road signs in real time using YOLO and CNN deep learning models, visualizes driving context via Google Street View, and logs compliance data for analysis.
The application is built as a full-stack solution, including:

A Python-based YOLO model for sign detection and classification

A C# backend for data logging, storage, and AI orchestration

A client-facing Angular web application for visualization, alerts, and interaction

🧠 YOLO-Based AI Model (Python)
The core of the AI engine relies on YOLOv8 for real-time object detection. The model has been trained to recognize a wide variety of traffic signs, including:

Stop signs

Speed limit signs

Yield and priority signs

No-entry and direction signs

✨ Model Features
Real-time performance: Optimized for fast frame-by-frame inference on live video.

High accuracy: Achieved over 92% mAP on the custom dataset of traffic signs.

Flexible input: Supports both video streams and still images.

Expandable: Easily extendable to other road elements (e.g., pedestrians, lanes).

📈 Model Outputs
For each frame, the model returns:

List of detected objects with class labels and confidence scores

Bounding box coordinates

Timestamp

Frame index

🧩 Backend - C# & SQL Server
The backend is implemented in C# (.NET) and serves multiple responsibilities:

Orchestrating inference: Receives YOLO model outputs and checks for driver compliance (e.g., did the driver stop at a stop sign?)

Data storage: Uses SQL Server to log:

Detected signs

Timestamps and GPS coordinates

Driver responses

Compliance status

API layer: Exposes RESTful endpoints for Angular frontend to fetch detection logs, sign history, and compliance metrics

🛠️ Key Backend Features
Modular codebase (Services, Controllers, DTOs)

Token-based security (JWT) for API protection

Performance-optimized DB queries and indexing

💻 Frontend - Angular App
The Angular frontend acts as the user interface for:

Real-time sign visualization: Overlay detections on simulated driving video

Street View Integration: Shows the actual road segment using Google Maps API

Compliance Dashboard: Displays driver behavior over time

Data analytics: Graphs, tables, and alerts for reviewing performance

🌐 Key UI Features
Fully responsive design (desktop/mobile)

User role support (student / instructor)

Filterable detection history by sign type, date, and result

Visual comparison between actual road and detected signs

🔗 System Integration
Here’s how the components communicate:

YOLO (Python) processes each frame and outputs detection data.

The detection is sent via TCP/HTTP to the C# backend, where compliance is evaluated.

All data is stored in SQL Server.

The Angular client fetches data through secure REST APIs to present insights and visualizations.

Communication is asynchronous to ensure video flow is not interrupted, and the backend queues model results for scalable processing.

🧪 Results
Detection accuracy: >92% mAP on a validation set of over 3,000 traffic sign images.

System latency: <120ms from video frame to UI visualization (on local hardware).

User feedback: Positive engagement with the learning tool, especially in educational environments for demonstrating safe driving logic and real-world AI applications.

🚀 Future Work
Add support for lane detection and traffic light recognition

Enhance GPS-based tracking and trip replay

Deploy as a web-hosted demo on Azure/AWS

Extend to real-time vehicle control simulators

🤝 Contributions
Contributions and suggestions are welcome!
Feel free to open an issue, submit a pull request, or contact us with your ideas.
