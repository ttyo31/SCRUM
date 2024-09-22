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


@app.route('/WFHapplicationsManager/<mgr_id>', methods=['GET'])
def get_applications_manager(mgr_id):
    '''
    Returns existing WFH applications under a particular manager ID
    '''
    response = supabase.table('applications').select("*").eq("mgr_id", mgr_id).execute()
    if response.data:
        return jsonify(response.data), 200
    return jsonify({"error": "No applications found"}), 404



@app.route('/WFHapplicationsStaff/<staff_id>', methods=['GET'])
def get_applications_staff(staff_id):
    '''
    Returns existing WFH applications under a particular manager ID
    '''
    response = supabase.table('applications').select("*").eq("staff_id", staff_id).execute()
    if response.data:
        return jsonify(response.data), 200
    return jsonify({"error": "No applications found"}), 404


if __name__ == '__main__':
    app.run(debug=True)

