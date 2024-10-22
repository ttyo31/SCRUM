import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from flask import json

# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Test for US001 - Staff withdrawing pending application 
class US001_WithdrawApplicationTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True


    @patch('app.supabase')
    def test_withdraw_success(self, mock_supabase):
        # Mock a successful delete response from Supabase
        mock_response = MagicMock()
        mock_response.data = [{"staff_id": 1234, "wfh_date": "2024-10-27"}]
        mock_supabase.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

        # Simulate POST request to cancel WFH
        response = self.app.post('/api/withdraw_application', 
                                data=json.dumps({"wfh_date": "2024-10-27", "id": 1234}),
                                content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Record deleted successfully", response.data)

    @patch('app.supabase')
    def test_withdraw_server_error(self, mock_supabase):
        # Simulate an exception being raised by Supabase
        mock_supabase.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.side_effect = Exception('Database error')

        # Simulate POST request
        response = self.app.post('/api/withdraw_application', 
                                data=json.dumps({"wfh_date": "2024-10-27", "id": 1234}),
                                content_type='application/json')

        # Assert that a 500 status code is returned
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Error deleting the record", response.data)


if __name__ == '__main__':
    unittest.main()