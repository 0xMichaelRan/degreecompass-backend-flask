from flask import Flask
from flask_cors import CORS
from routes.major_routes import major_bp
import os
from dotenv import load_dotenv
from config.logging_config import setup_logging

# Setup logging before any other imports
setup_logging()

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(major_bp, url_prefix='/api')

if __name__ == '__main__':
    # Get the API port from environment variables, default to 5001 if not set
    port = int(os.getenv('BACKEND_PORT', 5001))
    print(f"Running on port: {port}")
    app.run(debug=True, port=port)
