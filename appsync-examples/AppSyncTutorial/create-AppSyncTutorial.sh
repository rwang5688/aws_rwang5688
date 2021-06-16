#!/bin/bash
aws cloudformation create-stack \
    --stack-name AppSyncTutorial \
    --template-body file://AmazonDynamoDBCFTemplate.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters file://AppSyncTutorial-parameters.json \
    --region us-east-1

