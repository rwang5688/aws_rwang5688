#!/bin/bash
export MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_HOME/templates

# print environment variables
echo "MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_TEMPLATES"

# execute
echo "update-mindLAMP-platform in region=$1 with configuration=$2"
aws cloudformation update-stack --stack-name mindLAMP-platform-$1-$2 \
--template-body file://$MINDLAMP_PLATFORM_TEMPLATES/mindLAMP-platform.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://mindLAMP-platform-parameters-$2.json \
--region $1

