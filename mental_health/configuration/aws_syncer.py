import boto3
import os

class AWSS3Sync:  
    
    
    
    def sync_folder_to_s3(self, s3_bucket, filepath, filename):
        local_file_path = os.path.join(filepath, filename)
        s3_key = filename  # Adjust this if you need a different key structure in the bucket
        self.s3_client.upload_file(local_file_path, s3_bucket, s3_key)
        print(f"Uploaded {local_file_path} to s3://{s3_bucket}/{s3_key}")

    def sync_folder_from_s3(self, s3_bucket, filename, destination):
        local_file_path = os.path.join(destination, filename)
        s3_key = filename  # Adjust this if the key structure in the bucket is different
        self.s3_client.download_file(s3_bucket, s3_key, local_file_path)
        print(f"Downloaded s3://{s3_bucket}/{s3_key} to {local_file_path}")
