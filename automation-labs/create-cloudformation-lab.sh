#!/bin/bash
aws cloudformation create-stack --stack-name cloudformation-lab \
--template-body file://cloudformation-lab.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://cloudformation-lab-parameters.json
