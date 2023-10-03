echo %1
aws s3api create-bucket --bucket %1 --region us-east-1
aws s3api put-object --bucket %1 --key logs/jan/02.txt --body logs/jan/02.txt
aws s3api put-object --bucket %1 --key logs/jan/01.txt --body logs/jan/01.txt
aws s3api put-bucket-versioning --bucket %1 --versioning-configuration Status=Enabled
