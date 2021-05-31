#!/bin/bash
aws cloudformation create-stack --stack-name mywebapp-ec2-instance \
--template-body file://mywebapp-ec2-instance.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://mywebapp-ec2-instance-parameters.json \
--region us-east-2

