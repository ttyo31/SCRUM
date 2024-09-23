import os
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
# from config import Config
from supabase import create_client, Client  
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

CORS(app)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class Manager(db.Model):
    __tablename__ = "manager"
    MGR_ID = db.Column(db.Integer, primary_key = True,name="id")
    MGR_LNAME = db.Column(db.String(50), nullable=False, name = "lname")
    MGR_FNAME = db.Column(db.String(50), nullable=False, name = "fname")
    MGR_EMAIL = db.Column(db.String(50), nullable=False, name = "email")
    MGR_WFM = db.Column(db.Date, nullable=False, name = "wfm")


class Application(db.Model):
    __tablename__ = "applications"
    STAFF_ID = db.Column(db.Integer, primary_key=True, name="staff_id")
    MGR_ID = db.Column(db.Integer, primary_key=True, name ="mgr_id")
    WFH_date = db.Column(db.Date,primary_key= True, name ="wfh_date")
    APPROVAL = db.Column(db.Integer, name = "approval")
    def __repr__(self):
        return f"<staff_id={self.STAFF_ID}, reporting_manager={self.MGR_ID}, application_date={self.WFH_date}>"

class Employee(db.Model):
    __tablename__ = 'employee'  # Explicitly targeting the "employee" table
    Staff_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, name="staff_id")
    Staff_FName = db.Column(db.String(50), nullable=False, name = "staff_fname")
    Staff_LName = db.Column(db.String(50), nullable=False, name = "staff_lname")
    Dept = db.Column(db.String(50), nullable=False,name = "dept")
    Position = db.Column(db.String(50), nullable=False,name="position")
    Country = db.Column(db.String(50), nullable=False,name ="country")
    Email = db.Column(db.String(50), nullable=False,name ="email")
    Reporting_Manager = db.Column(db.Integer, nullable=True, name="reporting_manager")  # Nullable if some staff may not have a manager
    Role = db.Column(db.Integer, nullable=False,name ="role")

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
    

@app.route('/sendrequest/<int:staff_id>',methods=['POST'])
def send_request(staff_id):
    date = request.get_json()
    application_date = datetime.fromisoformat(date["date"])
    employee = Employee.query.filter_by(Staff_ID=staff_id).first()
    if not employee:
        return jsonify({'success': False, 'message': 'Employee not found'}), 404

    reporting_manager = employee.Reporting_Manager
    new_application = Application(
        STAFF_ID = staff_id,
        MGR_ID = employee.Reporting_Manager,
        WFH_date = date["date"],
        APPROVAL = 0
        )
    print(new_application)
    db.session.add(new_application)
    try:
        db.session.commit()
        print(new_application)  # This will use the __repr__ method to print the object
        return jsonify({'success': True, 'message': 'Application successfully added', 'application': str(new_application)}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Failed to add application', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,port=5001)
