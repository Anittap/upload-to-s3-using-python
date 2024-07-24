import os
import boto3
from botocore.exceptions import NoCredentialsError

def upload_files(directory, bucket_name):
  
  s3_client = boto3.client('s3')

  for root, dirs, files in os.walk(directory):
        
    for file_name in files:
      local_path = os.path.join(root, file_name)
      relative_path = os.path.relpath(local_path, directory)
      s3_path = relative_path.replace("\\", "/")  

      try:
          
        print(f'Uploading {local_path} to s3://{bucket_name}/{s3_path}')
        s3_client.upload_file(local_path, bucket_name, s3_path)

        s3_client.put_object_tagging(
            Bucket=bucket_name,
            Key=s3_path,
            Tagging={
                'TagSet': [
                            {'Key': 'Project', 'Value': 'shopping'} ,
                            {'Key': 'Owner', 'Value': 'anitta'},
                            {'Key': 'Env', 'Value': 'production'}
                          ]
            }
        )

        
      except FileNotFoundError:
          
        print(f'The file was not found: {local_path}')
          
      except NoCredentialsError:
          
        print('Credentials not available')


  
local_directory = './images/'  
s3_bucket = 'iamrole.anitta.cloud'

upload_files(local_directory, s3_bucket)
