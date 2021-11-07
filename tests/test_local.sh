#!/bin/bash

echo "Getting bucket name and function name from a cloudformation stack definition..."

KEY="landing/1.jpg"
BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name ReceiptParserStack  \
    --query "Stacks[0].Outputs" \
    --output json | jq -rc '.[] | select(.OutputKey=="BucketName") | .OutputValue ')

FUNCTION_NAME_LONG=$(aws cloudformation describe-stacks \
    --stack-name ReceiptParserStack  \
    --query "Stacks[0].Outputs" \
    --output json | jq -rc '.[] | select(.OutputKey=="FunctionName") | .OutputValue ')

FUNCTION_NAME=$(echo ${FUNCTION_NAME_LONG} | cut -d'-' -f 2)

echo "BUCKET_NAME - ${BUCKET_NAME}"
echo "FUNCTION_NAME - ${FUNCTION_NAME}"

echo "Generating SAM template..."
cdk synth --no-staging > template.yaml

echo "Running a test..."
sam local generate-event s3 put --bucket ${BUCKET_NAME} --key "$KEY"  | sam local invoke -e - "$FUNCTION_NAME"