import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request, jsonify
from flask import json

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Test for US001 - Staff withdrawing pending application 
class US016_WithdrawWFHTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    

    @patch('app.supabase')
    def test_withdraw_success(self, mock_supabase):
        mock_delete_response = MagicMock()
        mock_delete_response.data = [{"staff_id": 1234, "wfh_date": "2024-10-27"}]
        mock_supabase.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value = mock_delete_response

        # Mock a successful update response for the applications table
        mock_update_response = MagicMock()
        mock_update_response.data = [{"approval": 2}]
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.return_value = mock_update_response

        # Simulate POST request to cancel WFH
        response = self.app.post('/api/remove_wfh', 
                            data=json.dumps({"wfh_date": "2024-10-27", "id": 1234}),
                            content_type='application/json')

        # Check if the delete and update operations were successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Record deleted successfully", response.data)

        # Check if the delete and update methods were called with the correct arguments
        mock_supabase.table.assert_any_call("staff_wfh")  # Check call to "staff_wfh" table
        mock_supabase.table.assert_any_call("applications")  # Check call to "applications" table

        # Verify that the delete query is called with correct filters
        mock_supabase.table("staff_wfh").delete.return_value.eq.assert_called_with("id", 1234)
        mock_supabase.table("staff_wfh").delete.return_value.eq.return_value.eq.assert_called_with("wfh_date", "2024-10-27")

        # Verify the correct order of arguments in the update query:
        # First, staff_id should be checked
        mock_supabase.table("applications").update.return_value.eq.assert_called_with("staff_id", 1234)
        # Then, wfh_date should be checked
        mock_supabase.table("applications").update.return_value.eq.return_value.eq.assert_called_with("wfh_date", "2024-10-27")

        # Verify that the update is being done to set approval to 2
        mock_supabase.table("applications").update.assert_called_with({"approval": 2})

    @patch('app.supabase')
    def test_withdraw_no_matching_records(self, mock_supabase):
    # Mock a response where no records are found for deletion
        mock_delete_response = MagicMock()
        mock_delete_response.data = None  # Simulate no matching records
        mock_supabase.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value = mock_delete_response

    # Mock a response where no records are found for the update in the applications table
        mock_update_response = MagicMock()
        mock_update_response.data = None  # Simulate no matching records
        mock_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.return_value = mock_update_response

    # Simulate POST request to cancel WFH
        response = self.app.post('/api/remove_wfh',
                             data=json.dumps({"wfh_date": "2024-10-27", "id": 1234}),
                             content_type='application/json')

    # Check if the status code is still 200 (successfully processed, even though no records were found)
        self.assertEqual(response.status_code, 200)

    # Check if the response contains the message for no matching records found
        self.assertIn(b"No matching records found to delete", response.data)

    # Check if the delete and update methods were called with the correct arguments
        mock_supabase.table.assert_any_call("staff_wfh")  # Check call to "staff_wfh" table
        mock_supabase.table.assert_any_call("applications")  # Check call to "applications" table

    # Verify that the delete query was called with the correct filters
        mock_supabase.table("staff_wfh").delete.return_value.eq.assert_called_with("id", 1234)
        mock_supabase.table("staff_wfh").delete.return_value.eq.return_value.eq.assert_called_with("wfh_date", "2024-10-27")

    # Verify that the update query was called with the correct filters
        mock_supabase.table("applications").update.return_value.eq.assert_called_with("staff_id", 1234)
        mock_supabase.table("applications").update.return_value.eq.return_value.eq.assert_called_with("wfh_date", "2024-10-27")


if __name__ == '__main__':
    unittest.main()