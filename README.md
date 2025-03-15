# Areum Health Data Visualization App

A Python Flask application that visualizes health data from the Areum backend service.

## Features

- User authentication with JWT
- Interactive visualization of acceleration data
- Activity metrics calculation
- Multiple dataset selection
- Responsive UI with Bootstrap

## Requirements

- Python 3.9+
- Flask
- Pandas
- NumPy
- Plotly
- Requests

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/areum-visualization.git
cd areum-visualization
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the backend URL:
   - Open `app.py` and update the `API_BASE_URL` variable to point to your Areum backend

4. Run the application:
```bash
flask run
```

Or with Gunicorn (for production):
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## Docker Setup

This application can be run with Docker Compose alongside the backend services:

1. Make sure Docker and Docker Compose are installed on your system
2. Run the full stack:
```bash
docker-compose up -d
```

3. Access the visualization at `http://localhost:5000`

## Usage

1. Open the web application in your browser
2. Log in with your Areum credentials
3. View your acceleration data visualizations
4. Use the dropdown to select different datasets
5. Toggle between X/Y/Z components and magnitude views

## Screenshots

![Dashboard Screenshot](dashboard_screenshot.png)

## Important Notes

- This application requires the Areum backend to be running and accessible
- Make sure your backend API endpoints match the expected format
- For production deployment, update the Flask secret key and use HTTPS