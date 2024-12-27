import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone


@patch('your_module.get_client')
def test_get_restore_job_details(self, mock_get_client):
    # Mock AWS client and describe_restore_job response
    mock_backup_client = MagicMock()
    mock_get_client.return_value = mock_backup_client

    # Define mock response
    mock_response = {
        'CompletionDate': datetime(2024, 12, 24, 12, 34, 56, tzinfo=timezone.utc)
    }
    mock_backup_client.describe_restore_job.return_value = mock_response

    # Input arguments
    kwargs = {
        'Region': 'us-west-2',
        'RestoreJobId': 'mock-restore-job-id'
    }

    # Call the function
    result = get_restore_job_details(**kwargs)

    # Assertions
    mock_get_client.assert_called_once_with('backup', 'us-west-2')
    mock_backup_client.describe_restore_job.assert_called_once_with(RestoreJobId='mock-restore-job-id')
    self.assertEqual(result['RestoreJobId'], 'mock-restore-job-id')
    self.assertEqual(result['RestoreEndTime'], mock_response['CompletionDate'])

@patch('your_module.logger')
@patch('your_module.get_restore_job_details')
def test_log_metrics(self, mock_get_restore_job_details, mock_logger):
    # Mock the return value of get_restore_job_details
    mock_restore_job_details = {
        'RestoreJobId': 'mock-restore-job-id',
        'RestoreEndTime': datetime(2024, 12, 24, 12, 34, 56, tzinfo=timezone.utc)
    }
    mock_get_restore_job_details.return_value = mock_restore_job_details

    # Input arguments
    kwargs = {
        'Region': 'us-west-2',
        'RestoreJobId': 'mock-restore-job-id',
        'RestoreStartTime': datetime(2024, 12, 24, 11, 30, 0, tzinfo=timezone.utc),
        'NewFileSystemNane': 'mock-efs-name',
        'Filesize': 1024 ** 3  # 1 GB
    }

    # Call the function
    log_metrics(**kwargs)

    # Assertions
    mock_get_restore_job_details.assert_called_once_with(
        RestoreJobId='mock-restore-job-id', Region='us-west-2'
    )
    mock_logger.info.assert_any_call("EFS: mock-efs-name successfully restored. You rock!")
    mock_logger.info.assert_any_call("Restore Start Time: 2024-12-24 11:30:00+00:00")
    mock_logger.info.assert_any_call("Restore End Time: 2024-12-24 12:34:56+00:00")
    mock_logger.info.assert_any_call("Recovery Size: 1073741824")


