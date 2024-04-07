from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_read_main():
    response = client.get("/")  # Make a request to the root endpoint
    assert response.status_code == 200  # Check that the response status code is 200
    assert response.json() == {"message": "Hello World"}  # Check the response content