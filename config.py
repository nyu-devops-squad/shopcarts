import os
import json
import logging
from app.vcap_services import get_database_uri

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']
    print("Using VCAP_SERVICES")  # for debug purpose

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = get_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'secret-for-dev'
LOGGING_LEVEL = logging.INFO
