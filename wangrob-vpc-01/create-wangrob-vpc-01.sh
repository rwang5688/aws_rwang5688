#!/bin/bash
aws cloudformation create-stack --stack-name wangrob-vpc-01 \
--template-body file://wangrob-vpc-01.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://wangrob-vpc-01-parameters.json \
--region us-east-2

