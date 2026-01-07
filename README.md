# Inholland - Gym Exercise Detection & Analytics

Movement Recognition for Project Exploring AI - Streamlit Dashboard

## Overview

A Streamlit-based application that uses computer vision to detect gym exercises from video footage and provides comprehensive analytics dashboards for gym owners to track equipment usage, peak hours, and member activity patterns.

## Features

### Exercise Detection
- Real-time video analysis using Roboflow inference API
- Frame-by-frame processing with adjustable skip rate
- Confidence threshold filtering
- Live preview with bounding box visualization
- CSV export of detection results

### Analytics Dashboard
- Daily visitor trends and patterns
- Exercise popularity rankings
- Peak hour identification
- Day of week analysis
- Exercise heatmaps
- Busiest and slowest days tracking
- Data filtering by date range and exercise type
- Export functionality

## Supported Exercises

- Bench Press
- Lat Pulldown
- Leg Press
- Cable Row
- Shoulder Press
- Bicep Curl
- Tricep Pushdown
- Deadlift
- Squat Rack
- Chest Fly
- Leg Curl
- Calf Raise

## Project Structure

```
Inholland/
├── main.py                 # Main entry point with authentication
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
├── README.md
├── Data/                   # Data files
├── Plugins/
│   ├── app.py              # Exercise detection module
│   ├── Analytics.py        # Analytics dashboard module
│   └── gym_daily_exercise_stats.csv
└── .gitignore
```

## Installation

1. Clone the repository:
```
git clone https://github.com/nanxncndnx-glitch/Inholland.git
cd Inholland
```

2. Create virtual environment:
```
python -m venv venv
source venv/bin/activate
```
On Windows:
```
venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create .env file with your API key:
```
Api_Key=your_roboflow_api_key
```

## Requirements

- Python 3.9+
- streamlit
- opencv-python
- pandas
- plotly
- inference-sdk
- python-dotenv
- numpy
- Pillow

## Usage

Run the application:
```
streamlit run main.py
```

### Exercise Detection

1. Navigate to Exercise Detection in the menu
2. Enter your Roboflow API key
3. Set frame skip rate (higher = faster, fewer API calls)
4. Set confidence threshold
5. Upload video file (mp4, mov, avi, mkv)
6. Click Start Detection
7. View results and download CSV

### Analytics Dashboard

1. Navigate to Analytics in the menu
2. Use sidebar filters for date range and exercise type
3. View metrics, charts, and trends
4. Export data as needed

## Data Format

The analytics module expects CSV data with these columns:

- date: YYYY-MM-DD
- exercise: Exercise name
- total_persons: Number of users
- total_duration_minutes: Total time in minutes
- total_sets: Total sets performed
- total_reps: Total reps performed
- peak_hour: Busiest hour (HH:00)

## API

Uses Roboflow Inference API:
- Model: exercise-classification-agacq/7
- Endpoint: https://serverless.roboflow.com

Get your API key at: https://roboflow.com

## License

MIT License

## Author

nanxncndnx-glitch

## Acknowledgments

- Roboflow for the inference API
- Streamlit for the dashboard framework
- Plotly for interactive visualizations
