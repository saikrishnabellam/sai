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
