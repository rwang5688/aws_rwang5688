#!/bin/bash
. checkenv.sh

SERVICES=(resources crawler-service analysis-service ui-service)

function deploy () {
  for SERVICE in "${SERVICES[@]}"
  do
    echo ----------[ deploying $SERVICE ]----------
    cd $SERVICE
    if [ -f package.json ]; then
      npm install
    fi
    serverless deploy
    cd ..
  done
}

deploy

cd frontend-apps
aws s3 sync web-app/ s3://$IMAGE_ANALYSIS_APPS_BUCKET
cd ..
