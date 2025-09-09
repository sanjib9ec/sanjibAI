import requests
import boto3
import json
from datetime import datetime
import os

# -----------------------
# Configurations
# -----------------------
API_URL = "https://jsonplaceholder.typicode.com/posts"   # sample public API
S3_BUCKET = "your-s3-bucket-name"
S3_PREFIX = "api-ingestion/data"  # folder path in S3

# Optionally set via environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# -----------------------
# Fetch Data from API
# -----------------------
def fetch_api_data(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # raise error if failed
    return response.json()

# -----------------------
# Upload Data to S3
# -----------------------
def upload_to_s3(data, bucket, prefix):
    # Create S3 client
    s3 = boto3.client("s3", region_name=AWS_REGION)

    # Generate file name with timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_key = f"{prefix}/api_data_{timestamp}.json"

    # Convert data to JSON string
    json_data = json.dumps(data, indent=2)

    # Upload
    s3.put_object(
        Bucket=bucket,
        Key=s3_key,
        Body=json_data,
        ContentType="application/json"
    )

    print(f"✅ Data uploaded to s3://{bucket}/{s3_key}")

# -----------------------
# Main Execution
# -----------------------
if __name__ == "__main__":
    try:
        print("🔄 Fetching API data...")
        api_data = fetch_api_data(API_URL)

        print("⬆️ Uploading to S3...")
        upload_to_s3(api_data, S3_BUCKET, S3_PREFIX)

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
