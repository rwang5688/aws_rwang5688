#!/bin/bash
# push to application
aws deploy push --application-name mywebapp \
--s3-location s3://wangrob-code-pipeline-us-east-2/mywebapp/mywebapp.zip \
--ignore-hidden-files \
--source ../mywebapp \
--region us-east-2

