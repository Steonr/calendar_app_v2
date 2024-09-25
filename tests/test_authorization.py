import os
import pickle
import pytest
from unittest.mock import patch, mock_open, MagicMock, ANY
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from infra.authorization import AuthorizationService

@pytest.fixture
def mock_creds():
    creds = MagicMock(spec=Credentials)
    creds.valid = True
    creds.expired = False
    creds.refresh_token = 'mock_refresh_token'
    return creds

@pytest.mark.parametrize("token_exists, creds_valid, creds_expired, refresh_token, expected_refresh_call", [
    (True, True, False, 'mock_refresh_token', False),  # valid token
    (True, False, True, 'mock_refresh_token', True),   # expired token with refresh
    (False, False, False, None, True),                # no token file
], ids=[
    "valid_token",
    "expired_token_with_refresh",
    "no_token_file"
])
def test_get_credentials(token_exists, creds_valid, creds_expired, refresh_token, expected_refresh_call, mock_creds):
    # Arrange
    token_path = "./src/auth/gmail/token.pickle"
    secret_file_path = "./src/auth/gmail/client_secretfile.json"
    auth_service = AuthorizationService(token_path, secret_file_path)
    mock_creds.valid = creds_valid
    mock_creds.expired = creds_expired
    mock_creds.refresh_token = refresh_token

    with patch('os.path.exists', return_value=token_exists), \
         patch('builtins.open', mock_open()), \
         patch('pickle.load', return_value=mock_creds), \
         patch.object(auth_service, '_refresh_or_validate_credentials') as mock_refresh, \
         patch.object(auth_service, 'save_credentials') as mock_save:

        # Act
        auth_service.get_credentials()

        # Assert
        if expected_refresh_call:
            mock_refresh.assert_called_once()
            mock_save.assert_called_once()
        else:
            mock_refresh.assert_not_called()
       

@pytest.mark.parametrize("creds_expired, refresh_token, expected_refresh_call", [
    (True, 'mock_refresh_token', True),  # expired token with refresh
    (False, None, False),                # valid token
], ids=[
    "expired_token_with_refresh",
    "valid_token"
])
def test_refresh_or_validate_credentials(creds_expired, refresh_token, expected_refresh_call, mock_creds):
    # Arrange
    token_path = "./src/auth/gmail/token.pickle"
    secret_file_path = "./src/auth/gmail/client_secretfile.json"
    auth_service = AuthorizationService(token_path, secret_file_path)
    auth_service._creds = mock_creds
    mock_creds.expired = creds_expired
    mock_creds.refresh_token = refresh_token

    with patch.object(mock_creds, 'refresh') as mock_refresh, \
         patch.object(auth_service, '_validate_credentials', return_value=mock_creds) as mock_validate:

        # Act
        auth_service._refresh_or_validate_credentials()
        # Assert
        if expected_refresh_call:
            mock_refresh.assert_called_once_with(ANY)
        else:
            mock_refresh.assert_not_called()
            mock_validate.assert_called_once()

def test_validate_credentials():
    # Arrange
    token_path = "./src/auth/gmail/token.pickle"
    secret_file_path = "./src/auth/gmail/client_secretfile.json"
    auth_service = AuthorizationService(token_path, secret_file_path)
    mock_flow = MagicMock()
    mock_creds = MagicMock(spec=Credentials)

    with patch.object(InstalledAppFlow, 'from_client_secrets_file', return_value=mock_flow), \
         patch.object(mock_flow, 'run_local_server', return_value=mock_creds):

        # Act
        creds = auth_service._validate_credentials()

        # Assert
        assert creds == mock_creds


def test_save_credentials(mock_creds):
    # Arrange
    token_path = "./src/auth/gmail/token.pickle"
    secret_file_path = "./src/auth/gmail/client_secretfile.json"
    auth_service = AuthorizationService(token_path, secret_file_path)
    auth_service._creds = mock_creds

    with patch('builtins.open', mock_open()) as mock_file, \
         patch('pickle.dump') as mock_pickle_dump:

        # Act
        auth_service.save_credentials()

        # Assert
        mock_file.assert_called_once_with(token_path, "wb")
        mock_pickle_dump.assert_called_once_with(mock_creds, mock_file())
