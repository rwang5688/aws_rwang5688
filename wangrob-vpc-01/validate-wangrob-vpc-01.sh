#!/bin/bash
aws cloudformation validate-template --template-body file://wangrob-vpc-01.yaml \
--region us-west-2
