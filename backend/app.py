from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


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

if __name__ == '__main__':
    app.run(debug=True)
