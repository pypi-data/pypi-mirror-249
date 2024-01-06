# S3Adapter

A AWS S3 Python Adapter to Readn, Write and Check existence of files in S3 Buckets.
Current version use adapter to read/write a dataframe as csv in bucket

## Installation

You can install My Package using pip:

```bash
pip install s3adapter
```

## Usage
1. Set defatut AWS Account Environment vars (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION) or call ```s3adapter.init_cloud()``` method

2. Write your code like it to write an Dataframe to your bucket

```python
from fileadapters.s3adapter import s3adapter
import pandas as pd

bucket_name = <your-bucket>
# Creating a DataFrame from a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 22],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}

df = pd.DataFrame(data)

# Initialize Adapter with Bucket Name and option to validate if cloud credentials is configured
s3 = s3adapter(bucket_name, validade_aws=True)

# Write dataframe as CSV
s3.write_dataframe_as_csv(df,file_path)

```