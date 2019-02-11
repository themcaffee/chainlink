import os

# Attempt to get config from environment variables before default
# for the production environment
ENV = os.environ.get("ENV", default="development")
DEBUG = os.environ.get("DEBUG", default=True)
SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
if not SECRET_KEY:
    SECRET_KEY = os.urandom(16)
