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
    where approval is pending (approval == 0), along with the manager and staff names.
    '''
    try:
        # Fetch pending applications for the given manager
        response = supabase.table('applications')\
            .select("*")\
            .eq("mgr_id", mgr_id)\
            .eq("approval", 0)\
            .execute()

        if not response.data:
            return jsonify({"error": "No pending applications found"}), 404

        applications = response.data
        
        # Create a set of unique staff IDs and include manager ID
        staff_ids = {app['staff_id'] for app in applications}

        # Query employee table for staff names
        staff_response = supabase.table('employee')\
            .select("staff_id, staff_fname, staff_lname")\
            .in_("staff_id", list(staff_ids))\
            .execute()

        # Query employee table for manager names
        manager_response = supabase.table('employee')\
            .select("staff_id, staff_fname, staff_lname")\
            .eq("staff_id", mgr_id)\
            .execute()

        if not staff_response.data or not manager_response.data:
            return jsonify({"error": "No employee data found"}), 404

        # Combine employee names into a dictionary
        staff_data = {emp['staff_id']: f"{emp['staff_fname']} {emp['staff_lname']}" for emp in staff_response.data}

        # Extract the manager's name
        manager_name = f"{manager_response.data[0]['staff_fname']} {manager_response.data[0]['staff_lname']}"


        for app in applications:
            # Update staff_id to "id (name)"
            app['staff_id'] = f"{app['staff_id']} ({staff_data.get(app['staff_id'], 'Unknown')})"
    
            # Update mgr_id to "id (name)"
            app['mgr_id'] = f"{mgr_id} ({manager_name})"

        
        return jsonify(applications), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/WFHapplicationsStaff/<staff_id>', methods=['GET'])
def get_applications_staff(staff_id):
    '''
    Returns existing WFH applications under a particular staff ID
    '''
    try:
        # Fetch pending applications for the given staff
        response = supabase.table('applications').select("*").eq("staff_id", staff_id).execute()

        if not response.data:
            return jsonify({"error": "No pending applications found"}), 404

        applications = response.data
        
        # Create a set of unique mgr IDs and
        mgr_ids = {app['mgr_id'] for app in applications}

        # Query employee table for mgr names
        manager_response = supabase.table('employee')\
            .select("staff_id, staff_fname, staff_lname")\
            .in_("staff_id", list(mgr_ids))\
            .execute()

        # Query employee table for staff names
        staff_response = supabase.table('employee')\
            .select("staff_id, staff_fname, staff_lname")\
            .eq("staff_id", staff_id)\
            .execute()

        if not staff_response.data or not manager_response.data:
            return jsonify({"error": "No employee data found"}), 404

        # Combine employee names into a dictionary
        manager_data = {emp['staff_id']: f"{emp['staff_fname']} {emp['staff_lname']}" for emp in manager_response.data}

        # Extract the staff's name
        staff_name = f"{staff_response.data[0]['staff_fname']} {staff_response.data[0]['staff_lname']}"

        # Merge names into applications data
        for app in applications:
            app['mgr_id'] = f"{app['mgr_id']} ({manager_data.get(app['mgr_id'], 'Unknown')})"
            app['staff_id'] = f"{staff_id} ({staff_name})"  # Same staff for all applications in this context

        return jsonify(applications), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/approve_application', methods=['POST'])
def approve_application():
    data = request.get_json()
    # Extract integer part of staff_id and mgr_id by splitting the string
    staff_id = data['staff_id'].split()[0]  # Take the first part before the space
    mgr_id = data['mgr_id'].split()[0]      # Similarly, for mgr_id
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

        if staff_wfh_response.data:
            return jsonify({"success": True, "message": "Application approved and entry added to staff_wfh."}), 200
        
        return jsonify({"error": "Application approved, but failed to add entry to staff_wfh."}), 500
    
    return jsonify({"error": "Failed to approve application"}), 500

@app.route('/reject_application', methods=['POST'])
def reject_application():
    data = request.get_json()
    # Extract integer part of staff_id and mgr_id by splitting the string
    staff_id = data['staff_id'].split()[0]  # Take the first part before the space
    mgr_id = data['mgr_id'].split()[0]      # Similarly, for mgr_id
    wfh_date = data['wfh_date']

    # Update the application approval status in Supabase
    response = supabase.table('applications').update({"approval": 2}) \
        .eq("staff_id", staff_id) \
        .eq("mgr_id", mgr_id) \
        .eq("wfh_date", wfh_date) \
        .execute()

    if response.data:
        return jsonify({"success": True, "message": "Application rejected"}), 200
    
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

