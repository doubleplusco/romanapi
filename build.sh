#!/bin/sh

# cd into the code directory
cd /Users/mo/Documents/projects/romanapi.com/src

# create the code archive
zip -r /Users/mo/Documents/projects/romanapi.com/deploy/romanapi.zip .

# update the function on lambda and publish a new version
aws --region us-east-1 lambda update-function-code --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --zip-file fileb:///Users/mo/Documents/projects/romanapi.com/deploy/romanapi.zip --publish

# aliases
# aws --region us-east-1 lambda list-aliases --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert
# aws --region us-east-1 lambda delete-alias --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --name prod
# aws --region us-east-1 lambda create-alias --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --name prod --function-version 4 --description "production release"