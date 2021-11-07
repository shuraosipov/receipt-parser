#!/bin/bash

echo "Getting bucket name and function name from a cloudformation stack definition..."

TEST_FILE="static_assets/1.jpg"
BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name ReceiptParserStack  \
    --query "Stacks[0].Outputs" \
    --output json | jq -rc '.[] | select(.OutputKey=="BucketName") | .OutputValue ')

FUNCTION_NAME_LONG=$(aws cloudformation describe-stacks \
    --stack-name ReceiptParserStack  \
    --query "Stacks[0].Outputs" \
    --output json | jq -rc '.[] | select(.OutputKey=="FunctionName") | .OutputValue ')

FUNCTION_NAME=$(echo ${FUNCTION_NAME_LONG} | cut -d'-' -f 2)

echo "Uploading file to S3..."
aws s3 cp "$TEST_FILE" s3://${BUCKET_NAME}/landing/1.jpg
sleep 10
echo "Checking results..."
aws s3 cp s3://${BUCKET_NAME}/staging/1.jpg-analyzeexpenseresponse.txt response.txt
cat response.txt