#!/bin/bash
aws cloudformation update-stack --stack-name cloudformation-lab \
--template-body file://cloudformation-lab.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://cloudformation-lab-parameters.json
