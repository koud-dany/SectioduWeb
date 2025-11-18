import sys
import os

# Get the home directory
HOME = os.environ.get('HOME', '/home/username')

# Adjust paths for Hostinger's Python environment
INTERP = os.path.join(HOME, 'virtualenv', 'public_html', 'videovote', '3.8', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add project directory to Python path
project_path = os.path.join(HOME, 'public_html', 'videovote')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_path, '.env'))

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
