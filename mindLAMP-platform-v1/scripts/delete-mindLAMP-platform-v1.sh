#!/bin/bash
export MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_HOME/templates

# print environment variables
echo "MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_TEMPLATES"

# execute
echo "delete-mindLAMP-platform in region=$1 with configuration=$2"
aws cloudformation delete-stack --stack-name mindLAMP-platform-$1-$2 \
--region $1

