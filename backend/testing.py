import unittest
from unittest.mock import patch
from flask import json
from app import app 

class TestWorkFromHomeApplication(unittest.TestCase):

    def setUp(self):
        # Push an application context
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the Flask test client
        self.client = self.app.test_client()
        self.client.testing = True
    
    @patch('requests.post')  # Mock the external HTTP request
    def test_mail(self, mock_post):
        # Mock response for the external POST request
        mock_response = {
            'success': "true",
            "message": "The email has been sent"
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        # Send a POST request to the /send-email route via the test client
        response = self.client.post('/api/send-email',  
            data=json.dumps({"recipient": "example@example.com", "body": "Test email body"}), 
            content_type='application/json')

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response data
        response_data = json.loads(response.data)

        # Assert that the expected message is in the response
        self.assertIn('Email sent and POST request made successfully', response_data['message'])
    
    def test_mail_real_call(self): #This one needs the server to run to actually test
        # Send a POST request to the /send-email route to trigger the actual function
        response = self.client.post('/api/send-email',  
            data=json.dumps({"recipient": "scrumjacksim@gmail.com", "body": "Test email body"}), 
            content_type='application/json')

        # Assert that the status code is 200 (Success)
        self.assertEqual(response.status_code, 200)

        # Parse the response data
        response_data = json.loads(response.data)

        # Assert that the expected message is in the response
        self.assertIn('Email sent and POST request made successfully', response_data['message'])     


# Test for US06 - manager can approve and reject WFH request
class TestApproveReject(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.supabase')  # Mock the supabase client for approval
    def test_approve_application(self, mock_supabase):
        # Set up mock response for updating approval status
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = True
        
        # Set up mock response for inserting into staff_wfh table
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = True

        # Simulate a POST request to approve an application
        response = self.app.post('/api/approve_application', 
            data=json.dumps({
                "staff_id": "1", 
                "mgr_id": "100", 
                "wfh_date": "2023-10-15"
            }), 
            content_type='application/json')

        # Check if the approval response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Application approved and entry added to staff_wfh.", response.data)

    @patch('app.supabase')  # Mock the supabase client for rejection
    def test_reject_application(self, mock_supabase):
        # Set up mock response for updating approval status
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = True

        # Simulate a POST request to reject an application
        response = self.app.post('/api/reject_application', 
            data=json.dumps({
                "staff_id": "1", 
                "mgr_id": "100", 
                "wfh_date": "2023-10-15"
            }), 
            content_type='application/json')

        # Check if the rejection response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Application rejected", response.data)

    @patch('app.supabase')  # Mock the supabase client for failure case
    def test_approve_application_failure(self, mock_supabase):
        # Simulate failure for updating approval status
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = None

        # Simulate a POST request to approve an application with failure
        response = self.app.post('/api/approve_application', 
            data=json.dumps({
                "staff_id": "1", 
                "mgr_id": "100", 
                "wfh_date": "2023-10-15"
            }), 
            content_type='application/json')

        # Check if the failure response is correct
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Failed to approve application", response.data)

    @patch('app.supabase')  # Mock the supabase client for failure case
    def test_reject_application_failure(self, mock_supabase):
        # Simulate failure for updating rejection status
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = None

        # Simulate a POST request to reject an application with failure
        response = self.app.post('/api/reject_application', 
            data=json.dumps({
                "staff_id": "1", 
                "mgr_id": "100", 
                "wfh_date": "2023-10-15"
            }), 
            content_type='application/json')

        # Check if the failure response is correct
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Failed to reject application", response.data)

    @patch('app.supabase')  # Mock the supabase client to simulate staff_wfh insertion failure
    def test_approve_application_staff_wfh_insert_failure(self, mock_supabase):
        # Set up mock response for updating approval status (success)
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = True
        
        # Simulate failure for inserting into the staff_wfh table
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = None

        # Simulate a POST request to approve an application
        response = self.app.post('/api/approve_application', 
            data=json.dumps({
                "staff_id": "1", 
                "mgr_id": "100", 
                "wfh_date": "2023-10-15"
            }), 
            content_type='application/json')

        # Check if the failure response for staff_wfh insertion is correct
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Application approved, but failed to add entry to staff_wfh.", response.data)


# Test for US08 - Manager view schedule for all departments
class TestAllWFHEvents(unittest.TestCase): #OK

    @patch('app.supabase')
    def test_all_wfh_events_success(self, mock_supabase):
        # Mock staff data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"},
            {"id": 2, "fname": "Jane", "lname": "Smith", "dept": "Finance"}
        ]

        # Mock WFH events data
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value.data = [
            {"id": 1, "wfh_date": "2024-10-21"},
            {"id": 2, "wfh_date": "2024-10-22"}
        ]

        # Create a test client
        with app.test_client() as client:
            response = client.get('/api/all_wfh_events')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {"fname": "John", "lname": "Doe", "wfh_date": "2024-10-21", "dept": "IT", "empId": 1},
                {"fname": "Jane", "lname": "Smith", "wfh_date": "2024-10-22", "dept": "Finance", "empId": 2}
            ])

    @patch('app.supabase')
    def test_all_wfh_events_no_staff(self, mock_supabase):
        # Mock empty staff data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = []

        # Create a test client
        with app.test_client() as client:
            response = client.get('/api/all_wfh_events')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json, {"error": "No staff found"})

    @patch('app.supabase')
    def test_all_wfh_events_staff_error(self, mock_supabase):
        # Mock an error when fetching staff
        mock_supabase.table.return_value.select.return_value.execute.side_effect = Exception("Database error")

        # Create a test client
        with app.test_client() as client:
            response = client.get('/api/all_wfh_events')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json, {"error": "Error fetching staff: Database error"})

    @patch('app.supabase')
    def test_all_wfh_events_wfh_error(self, mock_supabase):
        # Mock staff data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"}
        ]

        # Mock an error when fetching WFH events
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.side_effect = Exception("Database error")

        # Create a test client
        with app.test_client() as client:
            response = client.get('/api/all_wfh_events')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json, {"error": "Error fetching WFH events: Database error"})

    @patch('app.supabase')
    def test_get_all_employees_success(self, mock_supabase):
        # Mock the employee data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"},
            {"id": 2, "fname": "Jane", "lname": "Smith", "dept": "Finance"}
        ]

        # Create a test client
        with app.test_client() as client:
            response = client.get('/api/all_employees')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"},
                {"id": 2, "fname": "Jane", "lname": "Smith", "dept": "Finance"}
            ])

    @patch('app.supabase')
    def test_get_all_employees_error(self, mock_supabase):
        # Mock an error when fetching employees
        mock_supabase.table.return_value.select.return_value.execute.side_effect = Exception("Database error")

        # Create a test client
        with app.test_client() as client:
            response = client.get('/api/all_employees')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json, {"error": "Database error"})

# yay i managed to save this - thank you cherrypickkkkk
# Test for US09 - Manager and Director view team schedule 
class TestWFHEvents(unittest.TestCase): #OK 

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.supabase')  # Mock the supabase client
    def test_get_wfh_events(self, mock_supabase):
        # Set up mock data to return for department and staff query
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"dept": "IT"}
        ]
        
        # Mock data for staff query
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"}
        ]
        
        # Mock data for staff_wfh query
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value.data = [
            {"id": 1, "wfh_date": "2023-10-01"}
        ]

        # Perform GET request to the endpoint
        response = self.app.get('/api/wfh_events/1')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"John", response.data)
        self.assertIn(b"Doe", response.data)
        self.assertIn(b"2023-10-01", response.data)

        
if __name__ == "__main__":
    unittest.main()
