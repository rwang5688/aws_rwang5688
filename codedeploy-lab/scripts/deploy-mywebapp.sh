#!/bin/bash
# push to application
aws deploy push --application-name mywebapp \
--s3-location s3://wangrob-codedeploy-bucket-us-east-2/mywebapp/mywebapp.zip \
--ignore-hidden-files \
--source ../mywebapp \
--region us-east-2

# deploy application
aws deploy create-deployment --application-name mywebapp \
--s3-location bucket=wangrob-codedeploy-bucket-us-east-2,key=mywebapp/mywebapp.zip,bundleType=zip \
--deployment-group-name mywebapp-deployment-group \
--region us-east-2

