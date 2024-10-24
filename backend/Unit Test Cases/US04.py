import sys
import os
import unittest
from unittest.mock import patch
from flask import json

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

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
