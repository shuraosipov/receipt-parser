import os
import boto3
from textractprettyprinter.t_pretty_print_expense import get_string
from textractprettyprinter.t_pretty_print_expense import Textract_Expense_Pretty_Print, Pretty_Print_Table_Format

"""
boto3 client for Amazon Texract
"""
textract = boto3.client(service_name='textract')

"""
Set the S3 Bucket Name and File name 
Please set the below variables to your S3 Location
"""
s3_source_bucket_name = "parsercdkstack-s3bucketfbfa637e-n9ssj7hhzgzk"
s3_request_file_name = "landing/1.jpg"
    
"""
Call the Textract AnalyzeExpense API with the input Expense Image in Amazon S3
"""
try:
    response = textract.analyze_expense(
        Document={
            'S3Object': {
                'Bucket': s3_source_bucket_name,
                'Name': s3_request_file_name
            }
        })
    """
    Call Amazon Pretty Printer get_string method to parse the response and print it in fancy_grid format. 
    You can set pretty print format to other types as well like csv, latex etc.
    """
    pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.csv)
        
    """
    Use the pretty printed string to save the response in storage of your choice. 
    Below is just printing it on stdout.
    """
    print(pretty_printed_string)    

except Exception as e_raise:
    print(e_raise)
    raise e_raise