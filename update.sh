#!/bin/sh

# update the base accordingly
BASE=/Users/mo/Documents/projects/romanapi

# cd into the code directory
cd $BASE/src

# create the target deployment dir if it doesn't already exist
mkdir -p $BASE/target

# create a random identifier
ID=$RANDOM

# create the code archive
zip -r $BASE/target/romanapi_$ID.zip .

# update the function on lambda and publish a new version
aws --region us-east-1 lambda update-function-code --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --zip-file fileb://$BASE/target/romanapi_$ID.zip --publish

# aliases
# aws --region us-east-1 lambda list-aliases --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert
# aws --region us-east-1 lambda create-alias --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --name v1 --function-version 20 --description "v1 release"
# aws --region us-east-1 lambda create-alias --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --name dev --function-version 20 --description "dev release"
# aws --region us-east-1 lambda delete-alias --function-name arn:aws:lambda:us-east-1:956618040296:function:roman_api_convert --name v1