import unittest
from unittest.mock import patch
from flask import json
from app import app 

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