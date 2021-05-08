#!/bin/bash
export MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_HOME/templates

# print environment variables
echo "MINDLAMP_PLATFORM_TEMPLATES=$MINDLAMP_PLATFORM_TEMPLATES"

# execute
echo "validate-mindLAMP-platform"
aws cloudformation validate-template --template-body file://$MINDLAMP_PLATFORM_TEMPLATES/mindLAMP-platform.yaml

