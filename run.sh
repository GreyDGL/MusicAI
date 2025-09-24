#!/bin/bash
python app.py &
echo "Flask app started on http://localhost:8080"
echo "PID: $!"
echo "Application is running. Visit http://localhost:8080 in your browser."