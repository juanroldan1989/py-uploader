# Creates a S3 Bucket and returns the bucket URL
#
# Usage:
# python check_s3_bucket.py
#
# Input:
# Enter a unique bucket name: my-unique-bucket

# Output:
# Checking if bucket 'my-unique-bucket' exists ...

# Bucket 'my-unique-bucket' does not exist. Creating bucket ...
# Bucket 'my-unique-bucket' created sucessfully.
# Bucket URL: https://my-unique-bucket.s3.amazonaws.com/

import boto3
import botocore

# AWS credentials
AWS_ACCESS_KEY = "xxxxx"
AWS_SECRET_KEY = "yyyyy"

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
