#!/bin/bash
aws cloudformation validate-template --template-body file://mindLAMP-platform.yaml \
--region us-east-2
