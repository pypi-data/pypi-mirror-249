import os

BACKEND_BASE_URL = 'http://localhost:8001' if os.environ.get('GS_DEV', '').lower() == 'true' else 'https://backend.goldenset.io'