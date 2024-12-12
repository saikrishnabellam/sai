def copy_file_system_policy(**kwargs):
    """
    Copy the file system policy from a source EFS file system to a target EFS file system.
    If the source does not have a specific policy, use a default policy.

    :param kwargs: Dictionary containing 'SourceFileSystemId', 'TargetFileSystemId', and 'Region'.
    """
    try:
        source_file_system_id = kwargs.get("SourceFileSystemId")
        target_file_system_id = kwargs.get("TargetFileSystemId")
        region = kwargs.get("Region")

        if not source_file_system_id or not target_file_system_id or not region:
            raise ValueError("SourceFileSystemId, TargetFileSystemId, and Region are required parameters.")

        # Initialize EFS client
        efs_client = get_client("efs", region)

        # Get the policy of the source file system
        try:
            source_policy_response = efs_client.describe_file_system_policy(
                FileSystemId=source_file_system_id
            )
            source_policy = source_policy_response.get("Policy")
        except efs_client.exceptions.FileSystemPolicyNotFound:
            source_policy = None

        # Use default policy if no specific policy is found
        if not source_policy:
            logger.warning(f"No specific policy found for source file system {source_file_system_id}. Using default policy.")
            source_policy = {
                "Sid": "DenyInSecureTransport",
                "Effect": "Deny",
                "Principal": {"AWS": "*"},
                "Action": "elasticfilesystem:*",
                "Resource": "*",
                "Condition": {
                    "Bool": {"aws:SecureTransport": "false"}
                }
            }

        # Apply the policy to the target file system
        efs_client.put_file_system_policy(
            FileSystemId=target_file_system_id,
            Policy=source_policy
        )

        logger.info(f"File system policy copied from {source_file_system_id} to {target_file_system_id}.")
    except Exception as e:
        raise RuntimeError(f"Failed to copy file system policy from {kwargs.get('SourceFileSystemId')} to {kwargs.get('TargetFileSystemId')}: {str(e)}")

@patch("module_name.get_client")
def test_copy_file_system_policy(self, mock_get_client):
    # Mock input parameters
    kwargs = {
        "SourceFileSystemId": "fs-12345",
        "TargetFileSystemId": "fs-67890",
        "Region": "us-west-2"
    }

    # Default policy to use if no specific policy is found
    default_policy_dict = {
        "Sid": "DenyInSecureTransport",
        "Effect": "Deny",
        "Principal": {"AWS": "*"},
        "Action": "elasticfilesystem:*",
        "Resource": "*",
        "Condition": {
            "Bool": {"aws:SecureTransport": "false"}
        }
    }
    default_policy = json.dumps(default_policy_dict)

    # Mock EFS client
    mock_efs_client = MagicMock()
    mock_get_client.side_effect = lambda service, region: mock_efs_client if service == "efs" else None

    # Simulate the source EFS having no specific policy by raising PolicyNotFound
    mock_efs_client.describe_file_system_policy.side_effect = (
        mock_efs_client.exceptions.PolicyNotFound
    )

    # Mock put_file_system_policy response
    mock_efs_client.put_file_system_policy.return_value = {}

    # Call the function
    copy_file_system_policy(**kwargs)

    # Assert describe_file_system_policy was called with the source file system
    mock_efs_client.describe_file_system_policy.assert_called_once_with(
        FileSystemId="fs-12345"
    )

    # Assert put_file_system_policy was called with the target file system and default policy
    mock_efs_client.put_file_system_policy.assert_called_once_with(
        FileSystemId="fs-67890",
        Policy=default_policy
    )

    # Verify get_client is called with the correct service and region
    mock_get_client.assert_called_with("efs", "us-west-2")


