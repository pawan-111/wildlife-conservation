# Wildlife Monitoring Dashboard

## Description
The Wildlife Monitoring Dashboard is a web application designed to visualize and monitor wildlife detection data using YOLO (You Only Look Once) object detection algorithms. The dashboard provides insights into various aspects of wildlife monitoring, including detection heatmaps, species distribution, population estimation, and security alerts.

## Features
- **Detection Heatmap**: Visualizes detection counts across different zones.
- **Species Distribution**: Displays the distribution of various species detected.
- **Population Estimation**: Estimates the population of detected species.
- **Security Alerts**: Provides alerts related to wildlife security.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python packages:
   ```bash
   pip install -r yolo_project/requirements.txt
   ```

3. Install the necessary Node.js packages for the dashboard:
   ```bash
   cd dashboard
   npm install
   ```

## Usage

1. Start the YOLO detection server:
   ```bash
   python yolo_project/web.py
   ```

2. Start the React dashboard:
   ```bash
   cd dashboard
   npm start
   ```

3. Open your web browser and navigate to `http://localhost:3000` to view the dashboard.

## Components
- **Dashboard**: The main component that aggregates various visualizations.
- **DetectionHeatmap**: Displays a heatmap of detections across different zones.
- **SpeciesDistribution**: Shows the distribution of species detected.
- **PopulationEstimation**: Provides estimates of species populations.
- **SecurityAlerts**: Displays alerts related to wildlife security.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
