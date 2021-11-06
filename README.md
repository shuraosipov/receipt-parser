# Receipt parser (Work in Progress)
This solution extracts text from the scanned groceries receipts, parses the text, and saves the results in tabular form to the S3 for further processing and analysis.

# General flow for data ingestion

1. Upload an original image to the S3 landing bucket to the `landing` folder and trigger a lambda function.
2. A lambda function extracts the text from the image and saves results back to the S3 to the `staging` folder as a CSV file.

# Configure credentials
Setup aws credentials via `aws configure` or define it via environment variables.
You can generate aws credentials in AWS Console.

# Configure virtual environment and install cdk modules

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Installing dependencies for a Lambda Layer 
This lambda function uses `amazon-textract-prettyprinter` and `amazon-textract-response-parser` libraries, so we would need to create a new lamba layer that will contain this library.

The command below will install necessary dependencies locally, then cdk app will create a new layer using this packages:
```
$ cd lambda-layer
$ bash create_new_layer.sh
```
Script output:
```
Test if necessary packages is installed...
Python 3.9.5
pip 21.1.1 from .venv/lib/python3.9/site-packages/pip (python 3.9)
Installing dependencies
<RESPONSE TRUNCATED FOR READABILITY>
Successfully installed amazon-textract-prettyprinter-0.0.10 amazon-textract-response-parser-0.1.20 boto3-1.19.12 botocore-1.22.12 jmespath-0.10.0 marshmallow-3.11.1 python-dateutil-2.8.2 s3transfer-0.5.0 six-1.16.0 tabulate-0.8.9 urllib3-1.26.7
Done!
```



# Deploy function and necessary resources
From the `receipt-parser` root directory:
```
cdk synth
cdk deploy

```

After successful deploy you should see output like this:
```
...

ReceiptParserStack

Outputs:
ReceiptParserStack.BucketName = receiptparserstack-s3bucketfbfa637e-1j835dh2u9yc1
ReceiptParserStack.FunctionName = ReceiptParserStack-MyLambdaCCE802FB-sUYyGjrSYO2i

Stack ARN:
arn:aws:cloudformation:us-east-1:419091122511:stack/ReceiptParserStack/a05f30a0-3ead-11ec-8e1b-0a805f5ab73f
```

# Test 
Upload a sample receipt from the `static_assets` folder to the bucket under the `landing` folder. Wait for a few seconds and check if a new file appeared in the `staging` folder on the same bucket.


## Useful Links
- https://aws.amazon.com/prescriptive-guidance
- https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing
- https://github.com/aws-samples/amazon-textract-code-samples
- https://github.com/aws-samples/amazon-textract-response-parser/tree/master/src-python
- https://aws.amazon.com/blogs/machine-learning/announcing-expanded-support-for-extracting-data-from-invoices-and-receipts-using-amazon-textract/
- https://github.com/aws-samples/amazon-textract-analyze-expense-processing-pipeline
- https://github.com/aws-samples/amazon-textract-textractor/tree/master/prettyprinter
