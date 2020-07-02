#!/bin/bash
. checkenv.sh

SERVICES=(ui-service crawler-service analysis-service resources)

function remove () {
  for SERVICE in "${SERVICES[@]}"
  do
    echo ----------[ removing $SERVICE ]----------
    cd $SERVICE
    serverless remove
    cd ..
  done
}

aws s3 rm s3://$IMAGE_ANALYSIS_DATA_BUCKET --recursive
aws s3 rm s3://$IMAGE_ANALYSIS_APPS_BUCKET --recursive
remove
