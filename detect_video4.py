import csv
from datetime import datetime

import cv2
import socketio
from ultralytics import YOLO

# Initialize WebSocket client
sio = socketio.Client()
sio.connect('http://localhost:5001')

# Initialize CSV file
csv_file = open('photo_detections.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'camera_id', 'species', 'count', 'threat_type', 'alert_status'])

# Load the YOLO model
model = YOLO('yolov8n.pt')

# Path to the photo file and camera ID
photo_path = "/Users/pawanvishwakarma/Desktop/p1/yolo_project/zone4/human.jpg"
camera_id = "cam4"

# Read the photo
frame = cv2.imread(photo_path)

# Run YOLO inference on the photo
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
    # Send WebSocket alert
    sio.emit('detection', {
        'class': 'person',
        'zone': camera_id,
        'confidence': detections.conf[0].item(),
        'timestamp': timestamp
    })
elif "gun" in detected_classes:
    threat_type = "gun"
    alert_status = "yes"
    # Send WebSocket alert
    sio.emit('detection', {
        'class': 'gun',
        'zone': camera_id,
        'confidence': detections.conf[0].item(),
        'timestamp': timestamp
    })


# Write to CSV
for species, count in species_count.items():
    csv_writer.writerow([timestamp, camera_id, species, count, threat_type, alert_status])

# Visualize the results on the photo
annotated_frame = results[0].plot()

# Display the annotated photo
cv2.imshow("YOLO Object Detection", annotated_frame)

# Wait for key press to close window
cv2.waitKey(0)

# Close windows
cv2.destroyAllWindows()

# Close CSV file
csv_file.close()

# Disconnect WebSocket
sio.disconnect()
