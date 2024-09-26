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
        # Add a new entry to the staff_wfh table
        staff_wfh_response = supabase.table('staff_wfh').insert({
            "id": staff_id,
            "wfh_date": wfh_date
        }).execute()

        supabase.table('applications').delete() \
        .eq("staff_id", staff_id) \
        .eq("mgr_id", mgr_id) \
        .eq("wfh_date", wfh_date) \
        .execute()

        if staff_wfh_response.data:
            return jsonify({"success": True, "message": "Application approved and entry added to staff_wfh."}), 200
        
        return jsonify({"error": "Application approved, but failed to add entry to staff_wfh."}), 500
    
    return jsonify({"error": "Failed to approve application"}), 500

@app.route('/reject_application', methods=['POST'])
def reject_application():
    data = request.get_json()
    staff_id = data['staff_id']
    mgr_id = data['mgr_id']
    wfh_date = data['wfh_date']

    # Delete the application from the applications table
    response = supabase.table('applications').delete() \
        .eq("staff_id", staff_id) \
        .eq("mgr_id", mgr_id) \
        .eq("wfh_date", wfh_date) \
        .execute()

    if response.data:
        return jsonify({"success": True, "message": "Application rejected and entry deleted."}), 200
    
    return jsonify({"error": "Failed to reject application"}), 500



@app.route('/api/wfh_events/<int:userID>', methods=['GET'])
def get_wfh_events(userID):
    #Returns department staff on WFH
    dept = supabase.table("staff").select("dept").eq("id", userID).execute().data

    staff_query = supabase.table("staff").select("id, fname, lname", "dept").eq("dept", dept[0]["dept"]).execute()
    staff_data = staff_query.data

    staff_ids = [staff['id'] for staff in staff_data]

    # Query staff_wfh based on staff IDs
    wfh_query = supabase.table("staff_wfh").select("id, wfh_date").in_("id", staff_ids).execute()

    # Merge the data from staff and staff_wfh
    wfh_events = []
    for wfh in wfh_query.data:
        staff_info = next((staff for staff in staff_data if staff['id'] == wfh['id']), None)
        if staff_info:
            wfh_events.append({
                "fname": staff_info['fname'],
                "lname": staff_info['lname'],
                "wfh_date": wfh["wfh_date"],
                "dept": staff_info['dept']
            })

    return jsonify(wfh_events)


@app.route('/api/all_wfh_events', methods=['GET'])
def all_wfh_events():
    try:
        # Fetch all staff members
        staff_query = supabase.table("staff").select("id, fname, lname, dept").execute()
        staff_data = staff_query.data
        if not staff_data:
            return jsonify({"error": "No staff found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching staff: {str(e)}"}), 500

    # Extract all staff IDs
    staff_ids = [staff['id'] for staff in staff_data]

    # Query WFH events for all staff
    try:
        wfh_query = supabase.table("staff_wfh").select("id, wfh_date").in_("id", staff_ids).execute()
        wfh_data = wfh_query.data
    except Exception as e:
        return jsonify({"error": f"Error fetching WFH events: {str(e)}"}), 500

    # Merge staff data with WFH events
    wfh_events = []
    for wfh in wfh_data:
        staff_info = next((staff for staff in staff_data if staff['id'] == wfh['id']), None)
        if staff_info:
            wfh_events.append({
                "fname": staff_info['fname'],
                "lname": staff_info['lname'],
                "wfh_date": wfh["wfh_date"],
                "dept": staff_info['dept']
            })

    return jsonify(wfh_events), 200

if __name__ == '__main__':
    app.run(debug=True)

