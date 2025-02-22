from google.cloud import storage
from datetime import datetime
import os

def rename_gcs_file(bucket_name, source_file_name):
    """
    Picks a file from Google Cloud Storage, renames it with current date/time,
    and uploads it back to the bucket.
    
    Args:
        bucket_name (str): Name of the GCS bucket
        source_file_name (str): Name of the file to be renamed
    
    Returns:
        str: New file name if successful, None if failed
    """
    try:
        # Initialize the GCS client
        storage_client = storage.Client()
        
        # Get the bucket
        bucket = storage_client.bucket(bucket_name)
        
        # Get the source blob (file)
        source_blob = bucket.blob(source_file_name)
        
        # Generate new file name with current date and time
        file_extension = os.path.splitext(source_file_name)[1]
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_file_name = f"{os.path.splitext(source_file_name)[0]}_{current_time}{file_extension}"
        
        # Create a new blob with the new name
        new_blob = bucket.blob(new_file_name)
        
        # Copy the source blob to the new blob
        token = storage_client.generate_signed_url(
            bucket_name=bucket_name,
            blob_name=source_file_name,
            version="v4",
            expiration=300,  # URL expires in 5 minutes
            method="GET"
        )
        new_blob.rewrite(source_blob)
        
        # Delete the original blob
        source_blob.delete()
        
        print(f"File renamed successfully from {source_file_name} to {new_file_name}")
        return new_file_name
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    BUCKET_NAME = "your-bucket-name"
    SOURCE_FILE = "example.txt"
    
    renamed_file = rename_gcs_file(BUCKET_NAME, SOURCE_FILE)
    if renamed_file:
        print("File renaming operation completed successfully")
    else:
        print("File renaming operation failed")
