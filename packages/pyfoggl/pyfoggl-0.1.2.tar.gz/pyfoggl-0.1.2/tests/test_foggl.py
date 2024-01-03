import logging
import pytest
from unittest.mock import MagicMock

from pyfoggl import Foggl, FogglRequestError

@pytest.fixture
def client():
    client = Foggl("my_foggl")
    client.set_auth("token")
    return client

@pytest.fixture
def mock_send_request(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(Foggl, "send_request", mock)
    return mock

def test_send_request_success(client, mock_send_request):
    mock_send_request.return_value.status_code = 200
    resp = client.send_request("GET", "endpoint")
    assert resp.status_code == 200

def test_get_state_json_error(client, mock_send_request, caplog):
    mock_send_request.return_value.status_code = 200
    mock_send_request.return_value.json.side_effect = ValueError

    with caplog.at_level(logging.ERROR):
        state = client.get_state()

    assert "Failed to parse JSON" in caplog.text
    assert state is None

def test_get_state_failure(client, mock_send_request):
    mock_send_request.return_value.status_code = 404
    
    state = client.get_state()
    assert state is None

def test_get_value_failure(client, mock_send_request):
    mock_send_request.return_value.status_code = 404
    
    value = client.get_value()
    assert value is None
