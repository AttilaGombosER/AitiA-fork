import pytest
from unittest.mock import patch, Mock
import subprocess
import os
from client import App

# Define a path for a test configuration file
TEST_CONFIG_PATH = '/home/levente/AITIA/AitiA/config.json'

@pytest.fixture(autouse=True)
def mock_picamera():
    with patch('client.Picamera2', Mock()) as mock:
        yield mock

def test_mount_nfs_success(mocker):
    app = App(TEST_CONFIG_PATH)
    # Mock the subprocess.run to simulate a successful mount command
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value = Mock(returncode=0)

    # Mock logging to prevent actual logging
    mock_logging_info = mocker.patch('logging.info')
    mock_logging_critical = mocker.patch('logging.critical')

    # Mock time.sleep to avoid actual sleep
    mocker.patch('time.sleep')

    # Call the function
    app.mount_nfs()

    # Check if subprocess.run was called once
    mock_run.assert_called_once_with(
        ['sudo', 'mount', '/mnt/nfs_share'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    # Check if logging.info was called with "Mount successful."
    mock_logging_info.assert_called_with("Mount successful.")

    # Ensure critical logging is not called
    mock_logging_critical.assert_not_called()

def test_mount_nfs_failure(mocker):
    app = App(TEST_CONFIG_PATH)
    # Mock the subprocess.run to simulate a failing mount command
    mock_run = mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd', stderr='error'))

    # Mock logging to prevent actual logging
    mock_logging_critical = mocker.patch('logging.critical')
    mock_logging_info = mocker.patch('logging.info')

    # Mock time.sleep to avoid actual sleep
    mocker.patch('time.sleep')

    # Mock exit to prevent actual exit
    mock_exit = mocker.patch('builtins.exit')

    # Call the function
    app.mount_nfs()

    # Check if subprocess.run was called once
    mock_run.assert_called_once_with(
        ['sudo', 'mount', '/mnt/nfs_share'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    # Check if critical logging was called with the error
    mock_logging_critical.assert_any_call(
        'An error occurred while mounting: Command \'cmd\' returned non-zero exit status 1.'
    )
    mock_logging_critical.assert_any_call('Error Output: error')

    # Ensure that exit(1) is called
    mock_exit.assert_called_once_with(1)

    # Ensure logging.info was not called with "Mount successful."
    mock_logging_info.assert_not_called()
