#!/bin/bash
. ./.env
. checkenv.sh


function remove () {
  for SERVICE in "${SERVICES[@]}"
  do
    echo ----------[ removing $SERVICE ]----------
    cd $SERVICE
    serverless remove
    cd ..
  done
}


function domain () {
  cd ui-service
  serverless delete_domain
  cd ..
}


# remove frontend apps and data
aws s3 rm s3://$IMAGE_ANALYSIS_DATA_BUCKET --recursive
aws s3 rm s3://$IMAGE_ANALYSIS_APPS_BUCKET --recursive

# remove functions and buckets
SERVICES=(ui-service analysis-service crawler-service resources)
remove

# delete ui-service api domain and db table
domain

