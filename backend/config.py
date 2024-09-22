# import os
# class Config:
    
#     # SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/db_spm'
#     # SQLALCHEMY_TRACK_MODIFICATIONS = False

#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # Flask settings
    DEBUG = os.environ.get('FLASK_DEBUG', True)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')

    # Supabase settings
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

    # You can also add any SQLAlchemy configurations here, if needed.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SUPABASE_DATABASE_URL')  # If using Supabase as a database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

