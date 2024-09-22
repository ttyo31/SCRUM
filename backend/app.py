import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


class Employee(db.Model):
    __tablename__ = 'employee'  # Explicitly targeting the "employee" table
    Staff_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Position = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Reporting_Manager = db.Column(db.Integer, nullable=True)  # Nullable if some staff may not have a manager
    Role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Employee {self.Staff_ID}: {self.Staff_FName} {self.Staff_LName}, {self.Position}>'





@app.route('/add_employee/<fname>/<lname>/<dept>/<position>/<country>/<email>/<role>', methods=['POST'])
def add_employee(fname, lname, dept, position, country, email, role):
    new_employee = Employee(
        Staff_FName=fname,
        Staff_LName=lname,
        Dept=dept,
        Position=position,
        Country=country,
        Email=email,
        Role=int(role)
    )
    db.session.add(new_employee)
    try:
        db.session.commit()
        inserted_data = Employee.query.filter_by(Email=email).first()
        return f"Added and verified employee: {inserted_data}"
    except Exception as e:
        db.session.rollback()
        return f"Failed to add employee: {e}", 500


@app.route('/list_employees', methods=['GET'])
def list_employees():
    try:
        employee_list = Employee.query.all()
        count = len(employee_list)  # Get the count of employees
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return f"Error retrieving employees: {e}", 500
    

@app.route('/WFHapplications/<mgr_id>', methods=['GET'])
def get_applications(mgr_id):
    '''
    Returns existing WFH applications under a particular manager ID
    '''
    response = supabase.table('applications').select("*").eq("mgr_id", mgr_id).execute()
    if response.data:
        return jsonify(response.data), 200
    return jsonify({"error": "No applications found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
