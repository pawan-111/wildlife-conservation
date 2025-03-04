import logging

import eventlet
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('websocket_errors.log'),
        logging.StreamHandler()
    ]
)

# Use eventlet for better WebSocket support
eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)

# Configure SocketIO with proper keep-alive settings
socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    logger=True,
                    engineio_logger=True,
                    ping_timeout=60,
                    ping_interval=25,
                    max_http_buffer_size=1000000,
                    async_mode='eventlet')

@app.route('/')
def index():
    return "WebSocket server is running"

@socketio.on('connect')
def handle_connect():
    try:
        logging.info(f'Client connected with SID: {request.sid}')
        logging.info(f'Total connected clients: {len(socketio.server.manager.rooms["/"])}')
    except Exception as e:
        logging.error(f"Error handling client connection: {str(e)}")

@socketio.on('disconnect')
def handle_disconnect():
    try:
        logging.info(f'Client disconnected with SID: {request.sid}')
        logging.info(f'Remaining connected clients: {len(socketio.server.manager.rooms["/"])}')
    except Exception as e:
        logging.error(f"Error handling client disconnection: {str(e)}")

@socketio.on('detection')
def handle_detection(detection):
    try:
        if not all(key in detection for key in ['class', 'confidence', 'zone']):
            raise ValueError("Invalid detection data format")

        logging.info(f"Detection received - Class: {detection['class']}, Confidence: {detection['confidence']:.2f}, Zone: {detection['zone']}")
        socketio.emit('detection', detection)
        logging.info("Broadcasted detection to all connected clients")
    except Exception as e:
        logging.error(f"Error handling detection: {str(e)}")

if __name__ == '__main__':
    print("Starting WebSocket server on port 5001")
    socketio.run(app,
                host='0.0.0.0',
                port=5001,
                use_reloader=False,
                debug=True)
