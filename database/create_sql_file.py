import csv

# Open the CSV file
with open('employeenew.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row
    next(csv_reader)
    
    # Open a new SQL file to write the SQL insert statements
    with open('import_data.sql', 'w') as sql_file:
        # Write table creation statement (if needed)
        sql_file.write('''CREATE TABLE IF NOT EXISTS Employee (
            Staff_ID INT PRIMARY KEY,
            Staff_FName VARCHAR(50) NOT NULL,
            Staff_LName VARCHAR(50) NOT NULL,
            Dept VARCHAR(50) NOT NULL,
            Position VARCHAR(50) NOT NULL,
            Country VARCHAR(50) NOT NULL,
            Email VARCHAR(50) NOT NULL,
            Reporting_Manager INT,
            Role INT NOT NULL
        );\n\n''')

        # Generate insert statements
        for row in csv_reader:
            sql_file.write(f"INSERT INTO Employee (Staff_ID, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role) "
                           f"VALUES ({row[0]}, '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', {row[7]}, {row[8]});\n")

print("SQL file with INSERT statements has been generated.")
