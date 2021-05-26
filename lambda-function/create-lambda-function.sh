#!/bin/bash
aws cloudformation create-stack --stack-name lambda-function \
--template-body file://lambda-function.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://lambda-function-parameters.json \
--region us-east-1

