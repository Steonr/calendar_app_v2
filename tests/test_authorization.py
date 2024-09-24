import pytest
from unittest.mock import patch, mock_open, MagicMock
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from infra.authorization import Authorization
@pytest.fixture
def mock_os_path_exists():
    with patch('os.path.exists') as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_credentials():
    with patch('google.oauth2.credentials.Credentials') as mock_creds:
        yield mock_creds

@pytest.fixture
def mock_installed_app_flow():
    with patch('google_auth_oauthlib.flow.InstalledAppFlow') as mock_flow:
        yield mock_flow

@pytest.fixture
def mock_open_file():
    with patch('builtins.open', mock_open()) as mock_file:
        yield mock_file

@pytest.mark.parametrize("token_exists, creds_valid, creds_expired, refresh_token, expected_creds", [
    (True, True, False, False, "valid_creds"),  # happy path with valid token
    (True, False, True, True, "refreshed_creds"),  # expired creds with refresh token
    (True, False, True, False, "new_creds"),  # expired creds without refresh token
    (False, False, False, False, "new_creds"),  # no token file
], ids=[
    "valid_token",
    "expired_with_refresh",
    "expired_no_refresh",
    "no_token_file"
])
def test_authorization(mock_os_path_exists, mock_credentials, mock_installed_app_flow, mock_open_file,
                       token_exists, creds_valid, creds_expired, refresh_token, expected_creds):
    # Arrange
    mock_os_path_exists.return_value = token_exists
    mock_creds_instance = MagicMock()
    mock_creds_instance.valid = creds_valid
    mock_creds_instance.expired = creds_expired
    mock_creds_instance.refresh_token = refresh_token
    mock_credentials.from_authorized_user_file.return_value = mock_creds_instance
    mock_credentials.return_value = mock_creds_instance
    mock_flow_instance = MagicMock()
    mock_installed_app_flow.from_client_secrets_file.return_value = mock_flow_instance
    mock_flow_instance.run_local_server.return_value = "new_creds"

    # Act
    auth = Authorization("token_path.json", "secret_file.json")

    # Assert
    if token_exists:
        mock_credentials.from_authorized_user_file.assert_called_once_with("token_path.json", "secret_file.json")
    else:
        mock_credentials.from_authorized_user_file.assert_not_called()

    if creds_expired and refresh_token:
        mock_creds_instance.refresh.assert_called_once_with(Request())
    elif not creds_valid:
        mock_flow_instance.run_local_server.assert_called_once_with(port=0)

    mock_open_file.assert_called_once_with("token_path.json", "w")
    mock_open_file().write.assert_called_once_with(expected_creds.to_json())