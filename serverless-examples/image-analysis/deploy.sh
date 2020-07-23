#!/bin/bash
. ./.env
. checkenv.sh


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


function domain () {
  cd ui-service
  npm install
  serverless create_domain
  cd ..
}


# create apps and data buckets
# deploy crawler-service and analysis-service
SERVICES=(resources crawler-service analysis-service)
deploy

# create ui-service API domain
# deploy ui-service API functions
domain
SERVICES=(ui-service)
deploy

# deploy frontend app
cd frontend-apps
npm install
aws s3 sync web-app/ s3://$IMAGE_ANALYSIS_APPS_BUCKET
cd ..

