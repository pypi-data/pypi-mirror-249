# firestoreupload.py

import firebase_admin
from firebase_admin import credentials, initialize_app, storage

class firestoreupload:
    def __init__(self, credentials_path, storage_bucket) -> None:
        """
        Initialize the FireStoreUpload class.

        :param credentials_path: Path to the Firebase service account credentials JSON file.
        :param storage_bucket: Firebase Storage bucket name.
        """
        self.credentials_path = credentials_path
        self.storage_bucket = storage_bucket

    def upload_file(self, local_file_path):
        """
        Upload a file to Firebase Storage.

        :param local_file_path: Path to the local file to be uploaded.
        """
        self.local_file_path = local_file_path
        try:
            # Initialize Firebase app with credentials and storage bucket
            cred = credentials.Certificate(self.credentials_path)
            initialize_app(cred, {'storageBucket': self.storage_bucket})

            # Get file name from the local file path
            fileName = local_file_path

            # Get reference to the default storage bucket
            bucket = storage.bucket()

            # Create a blob (object) in the bucket with the same name as the local file
            blob = bucket.blob(fileName)

            # Upload the file to Firebase Storage
            blob.upload_from_filename(fileName)

            # Make the uploaded file public
            blob.make_public()

            # Print success message with the file URL
            message = {
                'message': 'File Uploaded',
                'url': blob.public_url
            }
            print(message)

        except Exception as e:
            print(f"Error uploading file: {e}")
