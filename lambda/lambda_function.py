import os
import json
import boto3
from botocore.client import Config
import urllib.parse
from textractprettyprinter.t_pretty_print_expense import get_string
from textractprettyprinter.t_pretty_print_expense import Textract_Expense_Pretty_Print, Pretty_Print_Table_Format


textract = boto3.client(service_name='textract')
s3 = boto3.client('s3')

class AWSHelper:
    def getResource(self, name, awsRegion=None):
        config = Config(
            retries = dict(
                max_attempts = 30
            )
        )

        if(awsRegion):
            return boto3.resource(name, region_name=awsRegion, config=config)
        else:
            return boto3.resource(name, config=config)

class S3Helper:

    @staticmethod
    def writeToS3(content, bucketName, s3FileName, awsRegion=None):
        s3 = AWSHelper().getResource('s3', awsRegion)
        object = s3.Object(bucketName, s3FileName)
        object.put(Body=content)

def analyze_expences(bucket_name, object_name):
    """
    Call the Textract AnalyzeExpense API with the input Expense Image in Amazon S3
    """
    try:
        response = textract.analyze_expense(
            Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_name
                }
            })
        """
        Call Amazon Pretty Printer get_string method to parse the response and print it in fancy_grid format. 
        You can set pretty print format to other types as well like csv, latex etc.
        """
        pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.csv)
            
        return pretty_printed_string

    except Exception as e_raise:
        print(e_raise)
        raise e_raise

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    file_name = os.path.basename(key)
    print(bucket)
    print(key)
    print(file_name)


    # try:
    #     response = s3.get_object(Bucket=bucket, Key=key)
    #     print("CONTENT TYPE: " + response['ContentType'])
    #     return response['ContentType']
    # except Exception as e:
    #     print(e)
    #     print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
    #     raise e

    response = analyze_expences(bucket, key)    
    S3Helper.writeToS3(response, bucket, f"staging/{file_name}-analyzeexpenseresponse.txt")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully!')
    }