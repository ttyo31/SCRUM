import sys
import os
import unittest
from unittest.mock import patch
from flask import json

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

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

if __name__ == "__main__":
    unittest.main()
