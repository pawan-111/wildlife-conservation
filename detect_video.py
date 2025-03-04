import csv
import logging
import time
from datetime import datetime

import cv2
import socketio
from ultralytics import YOLO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('detection_errors.log'),
        logging.StreamHandler()
    ]
)

# Initialize WebSocket client with retry logic
sio = socketio.Client()
max_retries = 5
retry_delay = 2

for attempt in range(max_retries):
    try:
        sio.connect('http://localhost:5001')
        logging.info("Successfully connected to WebSocket server")
        break
    except Exception as e:
        if attempt == max_retries - 1:
            logging.error(f"Failed to connect to WebSocket server after {max_retries} attempts: {str(e)}")
            raise
        logging.warning(f"WebSocket connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

# Initialize CSV file
csv_file = open('detections.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'camera_id', 'species', 'count', 'threat_type', 'alert_status'])

# Load the YOLO model with error handling
try:
    model = YOLO('yolov8n.pt')
    logging.info("YOLO model loaded successfully")
except Exception as e:
    logging.error(f"Failed to load YOLO model: {str(e)}")
    raise

# Path to the video file and camera ID
video_path = "/Users/pawanvishwakarma/Desktop/p1/yolo_project/location1/elephant.mp4"
camera_id = "cam1"

# Open the video file with error handling
try:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Failed to open video file: {video_path}")
    logging.info(f"Successfully opened video file: {video_path}")
except Exception as e:
    logging.error(f"Video capture error: {str(e)}")
    raise

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results = model(frame)

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Process detection results
        detections = results[0].boxes
        class_names = results[0].names
        detected_classes = [class_names[int(cls)] for cls in detections.cls]

        # Count unique species
        species_count = {}
        for cls in detected_classes:
            species_count[cls] = species_count.get(cls, 0) + 1

        # Determine threat type and alert status
        threat_type = "none"
        alert_status = "no"
        if "person" in detected_classes:
            threat_type = "human"
            alert_status = "yes"
            # Send WebSocket alert with error handling
            try:
                sio.emit('detection', {
                    'class': 'person',
                    'zone': camera_id,
                    'confidence': detections.conf[0].item(),
                    'timestamp': timestamp
                })
                logging.info("Successfully sent WebSocket alert for person detection")
            except Exception as e:
                logging.error(f"Failed to send WebSocket alert: {str(e)}")
        elif "gun" in detected_classes:
            threat_type = "gun"
            alert_status = "yes"
            # Send WebSocket alert with error handling
            try:
                sio.emit('detection', {
                    'class': 'gun',
                    'zone': camera_id,
                    'confidence': detections.conf[0].item(),
                    'timestamp': timestamp
                })
                logging.info("Successfully sent WebSocket alert for gun detection")
            except Exception as e:
                logging.error(f"Failed to send WebSocket alert: {str(e)}")

        # Write to CSV
        for species, count in species_count.items():
            csv_writer.writerow([timestamp, camera_id, species, count, threat_type, alert_status])

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLO Object Detection", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the video ends
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()

# Close CSV file
csv_file.close()

# Disconnect WebSocket
sio.disconnect()
