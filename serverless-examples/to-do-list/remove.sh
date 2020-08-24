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
  cd todo-service
  serverless delete_domain
  cd ..
}


# remove frontend apps and data
aws s3 rm s3://${TO_DO_LIST_APPS_BUCKET} --recursive
aws s3 rm s3://${TO_DO_LIST_DATA_BUCKET} --recursive

# remove functions and buckets
SERVICES=(frontend todo-service resources)
remove

# delete todo-service api domain and db table
# delete user pool domain
domain
aws dynamodb delete-table --table-name todo-service-dev
. ./cognito.sh teardown

