"""Application entry point."""
import os
from app import create_app

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Get host and port from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    # Run the application
    app.run(host=host, port=port)
