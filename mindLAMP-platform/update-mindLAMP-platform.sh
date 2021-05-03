#!/bin/bash
aws cloudformation update-stack --stack-name mindLAMP-platform \
--template-body file://mindLAMP-platform.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://mindLAMP-platform-parameters.json \
--region us-east-2

