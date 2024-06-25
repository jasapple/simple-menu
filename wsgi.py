from app import create_app
import os

config_path = os.environ.get('CONFIG_PATH', 'config.ini')
app = create_app(config_path)