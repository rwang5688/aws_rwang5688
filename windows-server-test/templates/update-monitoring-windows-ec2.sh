#!/bin/bash
aws cloudformation update-stack --stack-name monitoring-windows-ec2 \
--template-body file://monitoring-windows-ec2.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://monitoring-windows-ec2-parameters.json \
--region us-east-1

