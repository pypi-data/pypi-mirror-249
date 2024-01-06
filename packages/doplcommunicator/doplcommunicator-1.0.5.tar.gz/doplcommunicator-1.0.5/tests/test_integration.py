from unittest.mock import Mock
import time

from doplcommunicator import DoplCommunicator
from doplcommunicator.controllerdata import ControllerData

def test_end_to_end():
    # Setup
    communicator = DoplCommunicator("http://localhost:3000")
    mock = Mock()
    communicator.on_joined_session(mock.on_joined_session)
    communicator.on_controller_data(mock.on_controller_data)

    # Test
    communicator.connect()
    time.sleep(1)
    expected_controller_data = ControllerData(True, 1, 1, 1, 1, 1, 1, 1)
    communicator.controller_data = expected_controller_data

    # Verify
    time.sleep(1)
    communicator.disconnect()

    mock.on_joined_session.assert_called_once()
    assert isinstance(mock.on_joined_session.call_args.args[0], int)
    
    mock.on_controller_data.assert_called_once()
    assert mock.on_controller_data.call_args.args[0] == expected_controller_data