import sys
import os

# File Manager Deployment Configuration for lasectionduweb.org
# Replace YOUR_USERNAME with your actual Hostinger username

# Standard Hostinger paths (you'll need your username)
HOME = '/home/YOUR_USERNAME'  # Replace YOUR_USERNAME with actual username from hPanel
PROJECT_PATH = os.path.join(HOME, 'public_html')

# Add project directory to Python path
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Try to activate virtual environment if it exists
venv_path = os.path.join(HOME, 'virtualenv', 'public_html', '3.11', 'bin', 'python3')
if os.path.exists(venv_path) and sys.executable != venv_path:
    os.execl(venv_path, venv_path, *sys.argv)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_PATH, '.env'))

# Set production environment
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONUNBUFFERED'] = '1'

# Import Flask application
# The variable 'application' is what Passenger looks for
from app import app as application

# Ensure proper logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    application.run()
