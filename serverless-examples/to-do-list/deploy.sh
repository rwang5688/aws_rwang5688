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
  cd todo-service
  npm install
  serverless create_domain
  cd ..
}


# create apps and data buckets
# (waht does frontend deploy do?)
# create user and identity pools
SERVICES=(resources frontend user-service)
deploy

# create user pool domain
# set user pool login and logout pages
# extract user pool arn for deploying todo-service
. ./cognito.sh setup

# create todo-service API domain
# deploy todo-service API functions
domain
SERVICES=(todo-service)
deploy

# pack frontend js into one file
# deploy frontend app
cd frontend
npm run build
aws s3 sync dist/ s3://$TO_DO_LIST_APPS_BUCKET
cd ..

