import unittest
from unittest.mock import patch
from myAppELO import calculate_expected_score, calculate_expected_score_route, app
from flask import render_template


class TestApp(unittest.TestCase):
    # Add your previous test_calculate_expected_score function here

    def test_calculate_expected_score_route(self):
        with app.test_client() as client:
            with patch('myAppELO.get_player_id') as mock_get_player_id, \
                    patch('myAppELO.calculate_expected_score') as mock_calculate_expected_score:
                # Set up the mock functions
                mock_get_player_id.return_value = (1, 2, 3, 4)
                mock_calculate_expected_score.return_value = (0.21982307214553784, 0.7801769278544621)

                # Call the function to be tested with a POST request and form data
                response = client.post('/calculate_odds', data={
                    'player1_name': 'Alice',
                    'player2_name': 'Bob',
                    'player3_name': 'Charlie',
                    'player4_name': 'David',
                    'game_date': '2023-03-18',
                })

                # Check that the expected values are present in the response data
                self.assertIn('0.21982307214553784', response.data.decode())
                self.assertIn('0.7801769278544621', response.data.decode())



if __name__ == "__main__":
    unittest.main()
