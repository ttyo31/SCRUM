import os
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_cors import CORS 
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# def getStaff():
#     response = supabase.table('staff').select('fname').execute()
#     return response.data

# print(getStaff())