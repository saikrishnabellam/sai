def get_source_file_system_arn(**kwargs) -> str:
    """
    Retrieves the Source EFS File System ARN based on the provided FileSystemID.

    :param kwargs: Contains 'FileSystemID' and 'Region'.
    :return: The ARN of the specified EFS file system.
    :raises RuntimeError: If the file system is not found or an error occurs during the API call.
    """
    try:
        # Extract parameters from kwargs
        file_system_id = kwargs.get('FileSystemID')
        region = kwargs.get('Region')

        if not file_system_id or not region:
            raise ValueError("Both 'FileSystemID' and 'Region' are required parameters.")

        # Initialize the EFS client
        efs_client = boto3.client("efs", region_name=region)

        # Fetch file system details
        response = efs_client.describe_file_systems(
            FileSystemId=file_system_id
        )

        # Extract the ARN from the response
        file_system_arn = response['FileSystems'][0]['FileSystemArn']
        logger.info(f"Retrieved Source File System ARN: {file_system_arn}")
        return file_system_arn

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve the source file system ARN for FileSystemID: {kwargs.get('FileSystemID')} "
                           f"in Region: {kwargs.get('Region')}. Error: {str(e)}")


@patch("my_efs_module.get_client")
def test_get_source_file_system_arn_success(self, mock_get_client):
    """Test successful retrieval of the EFS ARN."""
    # Arrange
    mock_efs_client = MagicMock()
    mock_efs_client.describe_file_systems.return_value = {
        "FileSystems": [
            {"FileSystemArn": "arn:aws:efs:us-east-1:123456789012:file-system/fs-12345"}
        ]
    }
    mock_get_client.return_value = mock_efs_client

    # Act
    result = get_source_file_system_arn(FileSystemID="fs-12345", Region="us-east-1")

    # Assert
    self.assertEqual(result, "arn:aws:efs:us-east-1:123456789012:file-system/fs-12345")
    mock_efs_client.describe_file_systems.assert_called_once_with(FileSystemId="fs-12345")

@patch("my_efs_module.get_client")
def test_get_source_file_system_arn_not_found(self, mock_get_client):
    """Test when the EFS file system is not found."""
    # Arrange
    mock_efs_client = MagicMock()
    error_response = {"Error": {"Code": "FileSystemNotFound", "Message": "Not Found"}}
    mock_efs_client.describe_file_systems.side_effect = Exception("FileSystemNotFound")
    mock_get_client.return_value = mock_efs_client

    # Act & Assert
    with self.assertRaises(RuntimeError) as context:
        get_source_file_system_arn(FileSystemID="fs-99999", Region="us-east-1")

    self.assertIn("Failed to retrieve the source file system ARN", str(context.exception))
    mock_efs_client.describe_file_systems.assert_called_once_with(FileSystemId="fs-99999")
