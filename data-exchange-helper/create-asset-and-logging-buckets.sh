#!/bin/bash
aws cloudformation create-stack --stack-name asset-and-logging-buckets \
--template-body file://asset-and-logging-buckets.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://asset-and-logging-buckets-parameters.json
