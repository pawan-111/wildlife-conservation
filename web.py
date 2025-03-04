import sys

import cv2
import socketio
from ultralytics import YOLO

# Create a Socket.IO client
sio = socketio.Client()

def main():
    try:
        # Connect to the WebSocket server
        print("Connecting to WebSocket server...")
        sio.connect('http://localhost:5001')
        print("Successfully connected to WebSocket server")

        # Load the YOLO model
        model = YOLO('runs/detect/animal_human_gun_vehicle_detection/weights/best.pt')

        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Error: Could not open webcam")

        print("Webcam detection started. Press 'q' to quit.")

        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from webcam")
                break

            # Perform detection
            results = model(frame)

            # Process results
            for result in results:
                boxes = result.boxes  # Boxes object for bbox outputs
                for box in boxes:
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    class_name = model.names[class_id]

                    # Send detection event for security-related classes
                    if class_name in ['gun', 'person']:
                        detection_data = {
                            'class': class_name,
                            'zone': 'Zone A',  # Update with actual zone if available
                            'confidence': confidence
                        }
                        print(f"Sending detection: {detection_data}")
                        sio.emit('detection', detection_data)

                    # Draw bounding box and label
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{class_name} {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Display frame
            cv2.imshow('YOLO Webcam Detection', frame)

            # Break loop on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Release resources if they were initialized
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("Webcam detection stopped.")

if __name__ == "__main__":
    main()
