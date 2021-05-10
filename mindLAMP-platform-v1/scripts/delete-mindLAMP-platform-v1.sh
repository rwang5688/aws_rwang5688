#!/bin/bash
export MINDLAMP_PLATFORM_V1_TEMPLATES=$MINDLAMP_PLATFORM_V1_HOME/templates

# print environment variables
echo "MINDLAMP_PLATFORM_V1_TEMPLATES=$MINDLAMP_PLATFORM_V1_TEMPLATES"

# execute
echo "delete-mindLAMP-platform in region=$1 with configuration=$2"
aws cloudformation delete-stack --stack-name mindLAMP-platform-v1-$1-$2 \
--region $1

