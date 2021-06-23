#!/bin/bash
aws cloudformation create-stack --stack-name docdb-full-stack \
--template-body file://docdb-full-stack.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://docdb-full-stack-parameters.json \
--region us-east-1

