#!/bin/bash

# Environment setup
source /Users/chao/.local/share/virtualenvs/CompetitiveSudoku-yfZFRE5T/bin/activate

# Add the project directory to sys.path for Python
PROJECT_DIR="/Users/chao/Desktop/Projects/CompetitiveSudoku"
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Start AI service
echo "Starting ai..."
python3 ai/ai_service.py &

# Backend setup and start
echo "Starting Backend..."
# python manage.py makemigrations
# python manage.py migrate
python3 backend/manage.py runserver &

# Start Redis 
echo "Starting Redis Server..."
redis-server &

# # # Frontend: Build and start
# cd "$PROJECT_DIR/frontend"
# # npm run build
# npm start

# Wait for user to terminate the script
read -p "Press Enter to stop..."

# Cleanup and exit
echo "Cleaning up..."
killall npm  # Terminate the npm process
killall python  # Terminate the Python process
killall redis-server  # Terminate the Redis server

echo "Script completed."
