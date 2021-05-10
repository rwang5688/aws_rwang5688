#!/bin/bash
export MINDLAMP_PLATFORM_V1_TEMPLATES=$MINDLAMP_PLATFORM_V1_HOME/templates

# print environment variables
echo "MINDLAMP_PLATFORM_V1_TEMPLATES=$MINDLAMP_PLATFORM_V1_TEMPLATES"

# execute
echo "validate-mindLAMP-platform"
aws cloudformation validate-template --template-body file://$MINDLAMP_PLATFORM_V1_TEMPLATES/mindLAMP-platform-v1.yaml

