#!/bin/bash
. ./.env
. checkenv.sh

SERVICES=(frontend resources todo-service user-service)

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

aws s3 rm s3://${TO_DO_LIST_APPS_BUCKET} --recursive
aws s3 rm s3://${TO_DO_LIST_DATA_BUCKET} --recursive
. ./cognito.sh teardown

domain
remove

aws dynamodb delete-table --table-name todo-service-dev

