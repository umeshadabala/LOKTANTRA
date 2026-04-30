"""
LOKTANTRA: The Sovereign Saga
Main entry point for the Flask application.

A production-grade interactive election simulator for India,
teaching civic literacy through 8 gamified levels grounded
in ECI Constitutional principles (Articles 324-329).
"""
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
