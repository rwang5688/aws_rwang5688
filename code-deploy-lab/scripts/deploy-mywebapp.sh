#!/bin/bash
# deploy application
aws deploy create-deployment --application-name mywebapp \
--s3-location bucket=wangrob-code-pipeline-us-east-2,key=mywebapp/mywebapp.zip,bundleType=zip \
--deployment-group-name mywebapp-deployment-group \
--region us-east-2

