import os
import tempfile
from google.cloud import storage
import importlib.util

def download_and_execute(bucket_name, file_name, class_name) -> type:
    print(f"starting download of: {file_name}")
    # Create a GCS client
    storage_client = storage.Client()

    # The name of the GCS bucket
    bucket = storage_client.get_bucket(bucket_name)

    # The path to the file in GCS
    blob = bucket.blob(file_name)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        # Download the file from GCS to the temp file
        blob.download_to_filename(temp_file.name)
        temp_file.close()

        # Dynamically import the module from the downloaded file
        spec = importlib.util.spec_from_file_location("email-http", temp_file.name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Run install_packages() to install dependencies
        module.install_packages()

        # Import the CloudRunEmailClient class
        class_def = getattr(module, class_name)

        # Now you can use CloudRunEmailClient as needed
        # Example:
        # client = CloudRunEmailClient()
        # response = client.send_email("to@example.com", "Test Subject", "Test Body")
        # print(response)

    # Optional: Delete the temp file if desired
    os.remove(temp_file.name)

    print(f"downloaded: {file_name}")
    return class_def