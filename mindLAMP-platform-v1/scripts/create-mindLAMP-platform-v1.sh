#!/bin/bash
export MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_HOME/templates

# print environment variables
echo "MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_TEMPLATES"

# execute
echo "create-mindLAMP-platform in region=$1 with configuration=$2"
aws cloudformation create-stack --stack-name mindLAMP-platform-$1-$2 \
--template-body file://$MINDLAMP_PLATFORM_TEMPLATES/mindLAMP-platform-v1.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://mindLAMP-platform-v1-parameters-$2.json \
--region $1

