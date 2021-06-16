#!/bin/bash
aws cloudformation create-stack \
    --stack-name WebForm \
    --template-body file://WebForm.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters file://WebForm-parameters.json \
    --region us-east-1

