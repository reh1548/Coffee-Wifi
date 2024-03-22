import os
import csv
import pytest
from flask import url_for
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import main
@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        yield client

def test_add_cafe(client):
    # Simulate a POST request with form data
    form_data = {
        'cafe': 'Test Cafe',
        'location_url': 'https://example.com',
        'open_time': '09:00',
        'closing_time': '18:00',
        'coffee_rating': '☕☕☕',
        'wifi_rating': '💪💪💪',
        'power_outlet_rating': '🔌🔌🔌',
        'submit': True
    }
    response = client.post('/add', data=form_data, follow_redirects=True)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200

    # Check if the new cafe is added to the CSV file
    with open(main.csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_data = list(csv_reader)
        assert len(csv_data) > 0  # Ensure there is at least one row in the CSV file
        assert csv_data[-1] == ['Test Cafe', 'https://example.com', '09:00', '18:00', '☕☕☕', '💪💪💪', '🔌🔌🔌']

    # Check if the response redirects to the cafes page
    assert b'<title>Cafes</title>' in response.data  # Assuming the title tag is present in the cafes page
