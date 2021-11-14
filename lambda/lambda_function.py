import os
import json
import boto3
from botocore.client import Config
import urllib.parse
from textractprettyprinter.t_pretty_print_expense import get_string
from textractprettyprinter.t_pretty_print_expense import Textract_Expense_Pretty_Print, Pretty_Print_Table_Format
import pandas as pd


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

def analyze_expences(bucket_name, object_name) -> str:
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
        Call Amazon Pretty Printer get_string method to parse the response and print it in csv format. 
        You can set pretty print format to other types as well like csv, latex etc.
        """
        pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.csv)
            
        return pretty_printed_string

    except Exception as e_raise:
        print(e_raise)
        raise e_raise


def prerry_print_response_to_csv(prerry_print_response) -> str:
    """
    Convert pretty print response from textract to csv
    """

    products = { 'TITLE':[], 'PRICE':[] }
    meta = {}

    # Read prerry_print_response line by line and extract necessary fields
    for row in prerry_print_response.splitlines():

        if "RespDate" in row:
            meta['DATE'] = row.split(",")[1]
                    
        if "VENDOR_NAME" in row:
            meta['VENDOR'] = row.split(",")[1]
        
        if "TOTAL AMOUNT" in row:
            meta['TOTAL'] = row.split(",")[1]
        
        if "TAX" in row:
            meta['TAX'] = row.split(",")[1]
        
        if "(ITEM)" in row:
            products['TITLE'].append(row.split(",")[0])
            products['PRICE'].append(row.split(",")[1])
    
    df = pd.DataFrame(products)
    df['VENDOR']=meta['VENDOR']
    df['DATE']=meta['DATE']        

    return df.to_csv(index=False)

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    file_name = os.path.basename(key)
    
    print(bucket)
    print(key)
    print(file_name)

    prerry_print_response = analyze_expences(bucket, key)
    table = prerry_print_response_to_csv(prerry_print_response)
    
    S3Helper.writeToS3(table, bucket, f"staging/{file_name}-analyzeexpenseresponse.txt")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully!')
    }