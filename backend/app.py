# use this as the main one instead 

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_cors import CORS 
from flask import Flask, jsonify, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime, timezone

# Load environment variables
from flask_mail import Mail, Message
import requests
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) #this is to allow requests from any origin 
app.config.from_object(Config)
# this is instantiated but not set, i'll comment this out to test first 
# db = SQLAlchemy(app)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'scrumjacksim@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'ihatescrum'  # Your email password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = int(os.environ.get('MAIL_DEBUG', 0))

mail = Mail(app)  # Initialize Mail only once
# def getStaff():
#     response = supabase.table('staff').select('fname').execute()
#     return response.data

#This the generic code for testing the sending of email. need to generate the rest for specific people
@app.route('/api/send-email', methods=['POST'])
def send_email():
    url = "https://script.google.com/macros/s/AKfycbxG3EnSYZAFLlS9qhRseObe08CsHT-PviqhzKm99cTDAn4vit3KUgbEKDnt2qGodpS0/exec"
    data = request.get_json()
    recipient = data.get("recipient")
    body = data.get("body")
    payload = {
        'recipient': recipient,
        "message":body
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': str(http_err)}), 500
    except Exception as err:
        return jsonify({'error': str(err)}), 500

    # Step 4: Return a response to the client
    return jsonify({'message': 'Email sent and POST request made successfully', 'external_response': response.json()}), 200


@app.before_request
def log_request_info():
    print(f"Request path: {request.path}")
    print(f"Request method: {request.method}")
    # print(f"Request data: {request.get_json()}")

@app.route('/')
def index():
    return 'backend is running!', 200

@app.route("/api/manageremail/<mgr_id>", methods=["GET"])
def get_application_manager_mail(mgr_id):
    try:
        response = supabase.table("manager")\
            .select("email")\
            .eq("id",mgr_id)\
            .execute()
        if response.data:
            manager_email = response.data[0]['email']  # Assuming the data is a list of dictionaries
            return jsonify({"email": manager_email}), 200
        else:
        # Handle the case where no manager is found or an error occurred
            return jsonify({"error": "Manager not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/WFHapplicationsManager/<mgr_id>', methods=['GET'])
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
            app['staff_id'] = f"{staff_data.get(app['staff_id'], 'Unknown')}"
    
            # Update mgr_id to "id (name)"
            app['mgr_id'] = f"{manager_name}"

        
        return jsonify(applications), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/WFHapplicationsStaff/<staff_id>', methods=['GET'])
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
        
        # Create a set of unique mgr IDs
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
        staff_name = f"{staff_response.data[0]['staff_fname']} {staff_response.data[0]['staff_lname']}"

        # Filter applications based on date_of_application
        current_date = datetime.now(timezone.utc).date()  # Current date in UTC
        filtered_applications = []

        for app in applications:
            date_of_application = datetime.strptime(app['date_of_application'], "%Y-%m-%d").date()
            days_difference = (current_date - date_of_application).days
            if days_difference <= 14:
                # Merge names into applications data
                app['mgr_id'] = f"{manager_data.get(app['mgr_id'], 'Unknown')}"
                app['staff_id'] = f"{staff_name}"
                filtered_applications.append(app)

        # Debugging: Print the final filtered applications list        
        print("Number of Filtered Applications:", len(filtered_applications))

        return jsonify(filtered_applications), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/api/approve_application', methods=['POST'])
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

@app.route('/api/reject_application', methods=['POST'])
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
                "dept": staff_info['dept'],
                "empId": wfh['id']
            })

    return jsonify(wfh_events), 200

# Endpoint to get all employees
@app.route('/api/all_employees', methods=['GET'])
def get_all_employees():
    try:
        # Query the 'employees' table from Supabase
        response = supabase.table("staff").select("id, fname, lname, dept").execute()

        # Extract data from response
        employees = response.data
        
        # Return the employee data as JSON
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/remove_wfh', methods=["POST"])
def remove_wfh():
    data=request.get_json()
    date = data["wfh_date"]
    id = data["id"]
    try:
        response = supabase.table("staff_wfh").delete().eq("id", id).eq("wfh_date", date).execute()
        response2 = supabase.table("applications").update({"approval": 2}).eq("staff_id", id).eq("wfh_date", date).execute()
        if response.data and response2.data:
          return ("Record deleted successfully:", response.data)
        else:
          return ("No matching records found to delete")
    except Exception as e:
        return ("Error Deleting the record",e)
    

@app.route('/api/withdraw_application', methods=["POST"])
def withdraw_application():
    data=request.get_json()
    date = data["wfh_date"]
    id = data["id"]
    try:
        response = supabase.table("applications").delete().eq("staff_id", id).eq("wfh_date", date).execute()
        if response.data:
          return jsonify({"message": "Record deleted successfully", "data": response.data}), 200
        else:
          return jsonify({"message": "No matching records found to delete"}), 404
    except Exception as e:
        return jsonify({"error": "Error deleting the record", "details": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

