#!/bin/bash
aws cloudformation create-stack --stack-name manifest-bucket \
--template-body file://manifest-bucket.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://manifest-bucket-parameters.json
