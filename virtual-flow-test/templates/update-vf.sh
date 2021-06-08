#!/bin/bash
aws cloudformation update-stack --stack-name vf \
--template-body file://vf.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://vf-parameters.json \
--region us-east-1

