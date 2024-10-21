import sys
import os
import unittest
from unittest.mock import patch
from flask import json

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class US003_WFHEventsTestCase(unittest.TestCase):

    @patch('app.supabase')  # Make sure the path to supabase matches your actual app structure
    def test_get_wfh_events(self, mock_supabase):
        # Mock the response for department lookup
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {'dept': 'Engineering'}
        ]

        # Mock the response for staff lookup
        staff_data = [
            {'id': 1, 'fname': 'John', 'lname': 'Doe', 'dept': 'Engineering'},
            {'id': 2, 'fname': 'Jane', 'lname': 'Smith', 'dept': 'Engineering'}
        ]
        
        # Set the return value for the staff query
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = staff_data

        # Mock the response for WFH events
        wfh_data = [
            {'id': 1, 'wfh_date': '2024-10-21'},
            {'id': 2, 'wfh_date': '2024-10-22'}
        ]
        
        # Set up the return for the WFH query
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value.data = wfh_data

        # Make a request to your endpoint
        with app.test_client() as client:
            response = client.get('/api/wfh_events/1')  # Adjust the userID as needed

        # Define the expected response
        expected_data = [
            {'fname': 'John', 'lname': 'Doe', 'wfh_date': '2024-10-21', 'dept': 'Engineering'},
            {'fname': 'Jane', 'lname': 'Smith', 'wfh_date': '2024-10-22', 'dept': 'Engineering'}
        ]

        # Verify the response data
        self.assertEqual(response.json, expected_data)

    @patch('app.supabase') 
    def test_get_wfh_events_no_wfh(self, mock_supabase):
        # Mock the response for department lookup
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {'dept': 'Marketing'}
        ]

        # Mock the response for staff lookup
        staff_data = [
            {'id': 3, 'fname': 'Alice', 'lname': 'Johnson', 'dept': 'Marketing'}
        ]
        
        # Set the return value for the staff query
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = staff_data

        # Mock the response for WFH events - no events for Marketing department
        wfh_data = [] 

        # Set up the return for the WFH query
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value.data = wfh_data

        # Make a request to your endpoint
        with app.test_client() as client:
            response = client.get('/api/wfh_events/3')  # Adjust the userID as needed

        # Define the expected response - should be an empty list
        expected_data = []

        # Verify the response data
        self.assertEqual(response.json, expected_data)

if __name__ == '__main__':
    unittest.main()
