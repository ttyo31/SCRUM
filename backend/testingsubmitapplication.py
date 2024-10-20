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

# unit test for US07 - i hope i'm doing it correctly
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
