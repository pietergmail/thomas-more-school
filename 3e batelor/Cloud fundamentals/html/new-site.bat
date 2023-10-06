aws s3api create-bucket --bucket %1 --create-bucket-configuration LocationConstraint=eu-west-1 --object-ownership BucketOwnerPreferred
aws s3api put-public-access-block --bucket %1 --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
aws s3api put-bucket-acl --bucket %1 --acl public-read
aws s3 cp index.html s3://%1
aws s3 cp error.html s3://%1
aws s3api put-object-acl --bucket %1 --key index.html --acl public-read
aws s3api put-object-acl --bucket %1 --key error.html --acl public-read
aws s3 website s3://%1 --index-document index.html --error-document error.html
echo Website address: http://%1.s3-website-us-east-1.amazonaws.com
