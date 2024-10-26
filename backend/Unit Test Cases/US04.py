import sys
import os
import unittest
from unittest.mock import patch
from flask import json

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Test for US04 - Staff view team schedule
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
    
    @patch('app.supabase')  # Mock the supabase instance
    def test_get_all_employees_success(self, mock_supabase):
        # Mocking the response from Supabase
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"},
            {"id": 2, "fname": "Jane", "lname": "Smith", "dept": "IT"}
        ]

        # Sending a GET request to the get_all_employees endpoint
        response = self.app.get('/api/all_employees')

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": 1, "fname": "John", "lname": "Doe", "dept": "IT"},
            {"id": 2, "fname": "Jane", "lname": "Smith", "dept": "IT"}
        ])

    @patch('app.supabase')  # Mock the supabase instance
    def test_get_all_employees_error(self, mock_supabase):
        # Mocking an exception in the Supabase call
        mock_supabase.table.return_value.select.return_value.execute.side_effect = Exception("Database error")

        # Sending a GET request to the get_all_employees endpoint
        response = self.app.get('/api/all_employees')

        # Check the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])
        
if __name__ == "__main__":
    unittest.main()
