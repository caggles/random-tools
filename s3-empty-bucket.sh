#! /bin/bash
echo "Clean S3 bucket script"

echo "Please wait while list of S3 objects is generated..."
./s3curl.pl --id=klab https://citz-dev-exchange.objectstore.gov.bc.ca/artifactory-klab-bucket3 | xmllint --format -| grep Key

# https://thesanguy.com/forum/topic/s3curl-script-to-empty-an-emc-ecs-bucket/
