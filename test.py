import os
from google.cloud import storage

# Set the environment variable (if not already set in your environment)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Insert Google json file"

# Create a client
storage_client = storage.Client()

# List buckets
buckets = list(storage_client.list_buckets())
print("Buckets:")
for bucket in buckets:
    print(bucket.name)
