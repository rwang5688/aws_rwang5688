#!/bin/bash
aws cloudformation create-stack --stack-name data-exchange-buckets \
--template-body file://data-exchange-buckets.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://data-exchange-buckets-parameters.json
