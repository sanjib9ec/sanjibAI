import requests
import pandas as pd
import boto3
import os

# --------------------------
# 1. API CONFIG Sanjib
# --------------------------
API_URL = "https://jsonplaceholder.typicode.com/posts"  # sample placeholder API

# --------------------------
# 2. FETCH DATA
# --------------------------
def fetch_data(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # throw error if bad response
    return response.json()

# --------------------------
# 3. TRANSFORM DATA
# --------------------------
def transform_data(data):
    # Convert list of dicts into pandas DataFrame
    df = pd.DataFrame(data)
    # Example transformation: keep only first 5 columns
    df = df.loc[:, ["userId", "id", "title", "body"]]
    return df

# --------------------------
# 4. SAVE LOCALLY
# --------------------------
def save_to_csv(df, file_path="output.csv"):
    df.to_csv(file_path, index=False)
    print(f"✅ Data saved locally to {file_path}")

# --------------------------
# 5. OPTIONAL: UPLOAD TO S3
# --------------------------
def upload_to_s3(file_path, bucket_name, s3_key):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"✅ File uploaded to s3://{bucket_name}/{s3_key}")

# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    raw_data = fetch_data(API_URL)
    df = transform_data(raw_data)
    save_to_csv(df)

    # Optional: Upload to S3 (uncomment if needed)
    # upload_to_s3("output.csv", bucket_name="your-bucket-name", s3_key="api_data/output.csv")
