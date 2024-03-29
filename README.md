# Receipt parser
This solution extracts text from the scanned groceries receipts, parses the text, and saves the results in tabular form to the S3 for further processing and analysis.
<img src="images/receipt_parser.png" width="640">

# General flow for data ingestion

1. Upload an original image to the S3 landing bucket to the `landing` folder and trigger a lambda function.
2. A lambda function extracts the text from the image and saves results back to the S3 to the `staging` folder as a CSV file.

# Setup

## Configure credentials
Setup aws credentials via `aws configure` or define it via environment variables.
You can generate aws credentials in AWS Console.

## Configure virtual environment and install cdk modules
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Create new Lambda Layer
From the app root folder:
```
$ cd build_scripts/
$ bash create_new_layer.sh config
```

You will see the following output:
```
Checking if necessary system packages is installed... Success!
Python version - python3.9
Package name - pandas-textract-reader-lambda-layer.zip
Building lambda layer in /tmp/tmp.nqoEObnXYl/python/lib/python3.9/site-packages/ folder
S3 bucket for storing lambda layer package - shuraosipov-lambda-layers
Installing dependencies...  Success!
Compiling the .zip file... Success!
Archive size is 45M
Uploading lambda layer package to S3... Success!
Publishing a layer...  Success!
Cleaning up... Success!
Enjoy your newly created layer - arn:aws:lambda:us-east-1:419091122511:layer:pandas-textract-reader:3
```

Find more details for configuring layer prerequisites [here](build_scripts/README.md)

## Configure your CDK app parameters
Copy lambda layer arn and update `layer_version_arn' parameter in `cdk.json` file.

# Deploy
From the `receipt-parser` root directory:
```
cdk synth
cdk deploy
```

After successful deploy you should see an output like this:
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
The command below will upload a sample image from the `static_assets` folder to the bucket under the `landing` folder. Wait for a few seconds and check if a new file appeared in the `staging` folder on the same bucket.

```
bash tests/test_remote.sh
```

You will see the following output:
```
Getting bucket name and function name from a cloudformation stack definition...
Uploading file to S3...
upload: static_assets/1.jpg to s3://receiptparserstack-s3bucketfbfa637e-1j835dh2u9yc1/landing/1.jpg
Checking results...
download: s3://receiptparserstack-s3bucketfbfa637e-1j835dh2u9yc1/staging/1.jpg-analyzeexpenseresponse.txt to ./response.txt
"TITLE","PRICE","VENDOR","DATE"
"MaesriTor Kha Scup(ITEM)","2.49(PRICE)","MART","03012021"
"MAESRI GFEEN CURRY(ITEM)","2.49(PRICE)","MART","03012021"
"TK Org Lite Coconu(ITEM)","4.49(PRICE)","MART","03012021"
"MaesriTor Kha Scup(ITEM)","2.49(PRICE)","MART","03012021"
"MaesriTor Kha Scup(ITEM)","2.49(PRICE)","MART","03012021"
"MaesriTor Kha Scup(ITEM)","2.49(PRICE)","MART","03012021"
"MaesriTor Kha Scup(ITEM)","2.49(PRICE)","MART","03012021"
"MAESRI GFEEN CURRY(ITEM)","2.49(PRICE)","MART","03012021"
"MASERI MESAMAN CJR(ITEM)","2.49(PRICE)","MART","03012021"
"TK Org Coconat Mil(ITEM)","4.49(PRICE)","MART","03012021"
"TK Org Coconut Mil(ITEM)","4.49(PRICE)","MART","03012021"
"MEIJI CHOCOLATE(ITEM)","4.99(PRICE)","MART","03012021"
"BBG SEAWEED SOUF(ITEM)","8.99(PRICE)","MART","03012021"
```


# Local testing
You can use SAM CLI to invoke and test this lambda function locally.

```
$ bash test/test.sh
```

You will get the following output:
```
Getting bucket name and function name from a cloudformation stack definition...
BUCKET_NAME - receiptparserstack-s3bucketfbfa637e-1j835dh2u9yc1
FUNCTION_NAME - MyLambdaCCE802FB
Generating SAM template...
Running a test...
Reading invoke payload from stdin (you can also pass it from file with --event)
Invoking lambda_function.lambda_handler (python3.9)
START RequestId: e7d99e53-3fbe-4efd-bd26-fb0b646edc2c Version: $LATEST
END RequestId: e7d99e53-3fbe-4efd-bd26-fb0b646edc2c
REPORT RequestId: e7d99e53-3fbe-4efd-bd26-fb0b646edc2c  Init Duration: 0.18 ms  Duration: 5111.17 ms    Billed Duration: 5112 ms     Memory Size: 128 MB     Max Memory Used: 128 MB
{"statusCode": 200, "body": "\"Processing completed successfully!\""}
```
Check this link to see how to install SAM ClI - https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html

# Tip
To speedup development process you can use the `--hotswap` flag with cdk deploy to attempt to update your AWS resources directly instead of generating a AWS CloudFormation changeset and deploying it.
```
$ cdk deploy --hotswap
```




## Useful Links
- https://aws.amazon.com/prescriptive-guidance
- https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing
- https://github.com/aws-samples/amazon-textract-code-samples
- https://github.com/aws-samples/amazon-textract-response-parser/tree/master/src-python
- https://aws.amazon.com/blogs/machine-learning/announcing-expanded-support-for-extracting-data-from-invoices-and-receipts-using-amazon-textract/
- https://github.com/aws-samples/amazon-textract-analyze-expense-processing-pipeline
- https://github.com/aws-samples/amazon-textract-textractor/tree/master/prettyprinter
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-generate-event.html
