import boto3
import botocore

from config import AWS_ACCESS_KEY, AWS_SECRET_KEY

# Initialize a session using AWS credentials
session = boto3.Session(
  aws_access_key_id=AWS_ACCESS_KEY,
  aws_secret_access_key=AWS_SECRET_KEY
)

s3 = session.resource('s3')

# read the bucket name from user input
bucket_name = input("Enter a unique bucket name: ")

print(f"Checking if bucket '{bucket_name}' exists ...")

try:
  # Check if the bucket exists
  s3.meta.client.head_bucket(Bucket=bucket_name)
  print(f"Bucket '{bucket_name} already exists.'")
except botocore.exceptions.ClientError as e:
  # if a 404 error is thrown, the bucket does not exist
  if e.response['Error']['Code'] == '404':
    print(f"Bucket '{bucket_name}' does not exist. Creating bucket ...")

    # Create S3 bucket
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created sucessfully.")
  else:
    # if there is another error, re-raise the exception
    raise

# Return bucket full URL
bucket_url = f"https://{bucket_name}.s3.amazonaws.com/"

print(f"Bucket URL: {bucket_url}")
