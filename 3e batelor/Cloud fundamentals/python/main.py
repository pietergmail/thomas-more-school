import datetime
import boto3
import psutil
from botocore.exceptions import NoCredentialsError


# Function to log CPU usage
def log_cpu_usage():
    cpu = []
    for _ in range(10):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu.append(cpu_percent)
    return cpu


# Function to create an HTML file with CPU usage data
def create_html_report(cpu):
    with open('results.html', 'w') as f:
        f.write("<html><body>")
        f.write("<h1>CPU Usage Report</h1>")
        f.write("<ul>")
        for idx, usage in enumerate(cpu):
            f.write(f"<li>Second {idx + 1}: {usage}%</li>")
        f.write("</ul>")
        f.write("</body></html>")


# Function to upload the HTML file to S3
def upload_to_s3(html_file):
    s3 = boto3.client('s3')
    bucket_name = 'r0745616-lab1'
    key = 'results.html'

    # Set the content type to text/html
    extra_args = {'ContentType': 'text/html'}

    try:
        s3.upload_file(html_file, bucket_name, key, ExtraArgs=extra_args)
        print(f"Uploaded {html_file} to S3 bucket: {bucket_name}/{key}")
        make_public(s3, bucket_name, key)
        allow_static_site(s3, bucket_name, key)
    except FileNotFoundError:
        print(f"The file {html_file} was not found.")
    except NoCredentialsError:
        print("AWS credentials not found.")


# Function that makes the file publicly accessible through a web browser
def make_public(s3, bucket_name, key):
    s3.put_object_acl(
        Bucket=bucket_name,
        Key=key,
        ACL='public-read'
    )


# Changes the bucket properties so it hosts results.html as a static site
def allow_static_site(s3, bucket_name, key):
    s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': key},
        }
    )


if __name__ == "__main__":
    cpu_usage = log_cpu_usage()
    create_html_report(cpu_usage)
    upload_to_s3('results.html')