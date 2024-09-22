import os
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_cors import CORS 
from flask import Flask, jsonify, request
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

@app.route('/approve_application', methods=['POST'])
def approve_application():
    data = request.get_json()
    staff_id = data['staff_id']
    mgr_id = data['mgr_id']
    wfh_date = data['wfh_date']

    # Update the application approval status in Supabase
    response = supabase.table('applications').update({"approval": 1}) \
        .eq("staff_id", staff_id) \
        .eq("mgr_id", mgr_id) \
        .eq("wfh_date", wfh_date) \
        .execute()

    if response.data:
        return jsonify({"success": True, "message": "Application approved successfully"}), 200
    return jsonify({"error": "Failed to approve application"}), 500

@app.route('/reject_application', methods=['POST'])
def reject_application():
    data = request.get_json()
    staff_id = data['staff_id']
    mgr_id = data['mgr_id']
    wfh_date = data['wfh_date']

    # Update the application approval status in Supabase
    response = supabase.table('applications').update({"approval": 2}) \
        .eq("staff_id", staff_id) \
        .eq("mgr_id", mgr_id) \
        .eq("wfh_date", wfh_date) \
        .execute()

    if response.data:
        return jsonify({"success": True, "message": "Application approved successfully"}), 200
    return jsonify({"error": "Failed to approve application"}), 500


if __name__ == '__main__':
    app.run(debug=True)

