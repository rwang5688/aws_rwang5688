#!/bin/bash
aws cloudformation update-stack --stack-name test-oh-onboard-account \
--template-body file://onboard-account.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://test-oh-onboard-account-parameters.json \
--region us-east-2

