import os
import json
import logging

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

SECRET_KEY = 'secret-for-dev'
LOGGING_LEVEL = logging.INFO
