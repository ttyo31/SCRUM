import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from flask import json
from datetime import datetime, timedelta

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestWFHApplicationStatus(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Generate specific dates for testing
        today = datetime.now().date()
        self.safely_within_14_days = (today - timedelta(days=10)).strftime('%Y-%m-%d')  # Safely within 14 days
        self.on_the_dot_14_days = (today - timedelta(days=14)).strftime('%Y-%m-%d')  # Exactly 14 days
        self.outside_14_days = (today - timedelta(days=15)).strftime('%Y-%m-%d')  # Outside 14 days

    @patch('app.supabase')  # Mock the supabase client
    def test_get_applications_status(self, mock_supabase):
        # Mock applications data with date_of_application for filtering
        mock_applications = [
            {'staff_id': 140003, 'mgr_id': 140894, 'approval': 1, 'wfh_date': '2024-09-05', 'date_of_application': self.safely_within_14_days},
            {'staff_id': 140003, 'mgr_id': 140894, 'approval': 2, 'wfh_date': '2024-09-03', 'date_of_application': self.on_the_dot_14_days},
            # This application should be filtered out due to an older date_of_application
            {'staff_id': 140003, 'mgr_id': 140894, 'approval': 0, 'wfh_date': '2024-09-10', 'date_of_application': self.outside_14_days}
        ]

        # Mock manager data
        mock_manager_response = [
            {'staff_id': 140894, 'staff_fname': 'Rahim', 'staff_lname': 'Khalid'}
        ]

        # Mock staff data
        mock_staff_response = [
            {'staff_id': 140003, 'staff_fname': 'Janice', 'staff_lname': 'Chan'}
        ]

        # Mock supabase responses for applications, staff, and manager data
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=mock_applications),  # For applications query
            MagicMock(data=mock_staff_response)  # For staff query
        ]
        
        # Mock the manager query using in_() for mgr_ids
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value = MagicMock(data=mock_manager_response)

        # Perform the API request
        response = self.app.get('/api/WFHapplicationsStaff/140003')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
        # Only applications within 14 days or exactly on the 14-day boundary should be returned
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['mgr_id'], '140894 (Rahim Khalid)')
        self.assertEqual(data[0]['staff_id'], '140003 (Janice Chan)')
        self.assertEqual(data[0]['wfh_date'], '2024-09-05')

    @patch('app.supabase')
    def test_no_applications_found(self, mock_supabase):
        # Mock empty applications data
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])

        # Perform the API request
        response = self.app.get('/api/WFHapplicationsStaff/140003')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "No pending applications found"})

    @patch('app.supabase')
    def test_no_employee_data_found(self, mock_supabase):
        # Mock applications data with results but no employee data
        mock_applications = [
            {'staff_id': 140003, 'mgr_id': 140894, 'approval': 1, 'wfh_date': '2024-09-05', 'date_of_application': self.safely_within_14_days}
        ]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=mock_applications),  # For applications query
            MagicMock(data=[])  # For staff query returning empty data
        ]
        # Mock empty manager data response
        mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value = MagicMock(data=[])

        # Perform the API request
        response = self.app.get('/api/WFHapplicationsStaff/140003')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"error": "No employee data found"})

    @patch('app.supabase')
    def test_internal_server_error(self, mock_supabase):
        # Simulate an exception in supabase query
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")

        # Perform the API request
        response = self.app.get('/api/WFHapplicationsStaff/140003')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data, {"error": "Database error"})

if __name__ == '__main__':
    unittest.main()
