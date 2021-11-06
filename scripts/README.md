# Receipt parser (Work in Progress)
Python script which uses Textract library to extract text from the image and display results in text.
It can be executed locally to test basic functionality of textract.

# Install dependencies
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Test 
```
$ python analyze_expense.py

╒══════════════════════════════════════╤═══════════════════╕
│ Key                                  │ Value             │
├──────────────────────────────────────┼───────────────────┤
│ (VENDOR_NAME)                        │ MART              │
├──────────────────────────────────────┼───────────────────┤
│ Resp Time:(OTHER)                    │ 130733            │
├──────────────────────────────────────┼───────────────────┤
│ RespDate:(OTHER)                     │ 03012021          │
├──────────────────────────────────────┼───────────────────┤
│ RESPONSE CODE:(OTHER)                │ AFPROVED          │
├──────────────────────────────────────┼───────────────────┤
│ MerchantID:0(OTHER)                  │                   │
├──────────────────────────────────────┼───────────────────┤
│ APPROVAL CODE:(OTHER)                │ 06775S            │
├──────────────────────────────────────┼───────────────────┤
│ MasterCard(OTHER)                    │ 47.37             │
├──────────────────────────────────────┼───────────────────┤
│ BALANCE(OTHER)                       │ 47.37             │
├──────────────────────────────────────┼───────────────────┤
│ ARC:00(OTHER)                        │                   │
├──────────────────────────────────────┼───────────────────┤
│ TOTAL NUMBER OF ITEMS SC.D =(OTHER)  │ 13                │
├──────────────────────────────────────┼───────────────────┤
│ CHANGE(OTHER)                        │ 0.00              │
├──────────────────────────────────────┼───────────────────┤
│ Your Cashier was(OTHER)              │ FERNANDA          │
├──────────────────────────────────────┼───────────────────┤
│ TC:(OTHER)                           │ CA9179BE1C9360.11 │
├──────────────────────────────────────┼───────────────────┤
│ ACCOUNT NUMBER :(OTHER)              │ ***********1032   │
├──────────────────────────────────────┼───────────────────┤
│ TSI(OTHER)                           │ 6800              │
├──────────────────────────────────────┼───────────────────┤
│ 01:07pm 311(OTHER)                   │ of                │
├──────────────────────────────────────┼───────────────────┤
│ APPLICATION LABEL(OTHER)             │ Master Card       │
├──────────────────────────────────────┼───────────────────┤
│ TVR:(OTHER)                          │ 8020008000        │
├──────────────────────────────────────┼───────────────────┤
│ 01:07pm 52 4(OTHER)                  │ 5 311             │
├──────────────────────────────────────┼───────────────────┤
│ TEL(OTHER)                           │ (857) 209-2747    │
├──────────────────────────────────────┼───────────────────┤
│ MasterCard Credi I -(OTHER)          │ C                 │
├──────────────────────────────────────┼───────────────────┤
│ Amount USD(OTHER)                    │ $47.37            │
├──────────────────────────────────────┼───────────────────┤
│ TOTAL AMOUNT:(TOTAL)                 │ $47.3"            │
├──────────────────────────────────────┼───────────────────┤
│ SEQUENCE NUMBER:(INVOICE_RECEIPT_ID) │ 3094              │
├──────────────────────────────────────┼───────────────────┤
│ TAX(TAX)                             │ 0.00              │
╘══════════════════════════════════════╧═══════════════════╛

╒══════════════════════════╤═════════════╕
│ MaesriTor Kha Scup(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MAESRI GFEEN CURRY(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ TK Org Lite Coconu(ITEM) │ 4.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MaesriTor Kha Scup(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MaesriTor Kha Scup(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MaesriTor Kha Scup(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MaesriTor Kha Scup(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MAESRI GFEEN CURRY(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MASERI MESAMAN CJR(ITEM) │ 2.49(PRICE) │
├──────────────────────────┼─────────────┤
│ TK Org Coconat Mil(ITEM) │ 4.49(PRICE) │
├──────────────────────────┼─────────────┤
│ TK Org Coconut Mil(ITEM) │ 4.49(PRICE) │
├──────────────────────────┼─────────────┤
│ MEIJI CHOCOLATE(ITEM)    │ 4.99(PRICE) │
├──────────────────────────┼─────────────┤
│ BBG SEAWEED SOUF(ITEM)   │ 8.99(PRICE) │
╘══════════════════════════╧═════════════╛
```


## Useful Links
- https://aws.amazon.com/prescriptive-guidance
- https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing
- https://github.com/aws-samples/amazon-textract-code-samples
- https://github.com/aws-samples/amazon-textract-response-parser/tree/master/src-python
- https://aws.amazon.com/blogs/machine-learning/announcing-expanded-support-for-extracting-data-from-invoices-and-receipts-using-amazon-textract/
- https://github.com/aws-samples/amazon-textract-analyze-expense-processing-pipeline
- https://github.com/aws-samples/amazon-textract-textractor/tree/master/prettyprinter












