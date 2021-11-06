#!/bin/bash

set -e # Exit immediately if a pipeline returns a non-zero status

check_package () {
    echo "Test if necessary packages is installed..."
    python --version 
    pip --version
}

check_package

PYTHON_VERSION="python3.9"
LAYER_PATH="python/lib/${PYTHON_VERSION}/site-packages/"
# PACKAGE_NAME="lambda-layer.zip"

echo "Installing dependencies"
pip install -r requirements.txt -t ${LAYER_PATH} && echo "Done!"

# echo "Compiling the .zip file"
# cd $WORKDIR && zip -r9 ${PACKAGE_NAME} .

# echo "Publishing a layer"
# aws lambda publish-layer-version \
#     --layer-name Amazon-Textract-Parsing-Library-Layer \
#     --description "Lambda layer containting amazon-textract-response-parser and amazon-textract-prettyprinter python libraries" \
#     --zip-file fileb://${PACKAGE_NAME} \
#     --compatible-runtimes ${PYTHON_VERSION}