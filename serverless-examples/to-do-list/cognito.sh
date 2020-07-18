# CAVEAT only works for single id pool and user pool i.e. clean account as per book
#!/bin/bash
. ./.env
. checkenv.sh

case $1 in
  setup)
    # echo '#>>'>>.env
    # export TO_DO_LIST_COGNITO_DOMAIN=$TO_DO_LIST_COGNITO_DOMAIN_BASE.auth.us-west-2.amazoncognito.com
    # echo TO_DO_LIST_COGNITO_DOMAIN=$TO_DO_LIST_COGNITO_DOMAIN>>.env

    # export TO_DO_LIST_USER_POOL_ID=`aws cognito-idp list-user-pools --max-results 1 | jq -r '.UserPools | .[0].Id'`
    # echo TO_DO_LIST_USER_POOL_ID=$TO_DO_LIST_USER_POOL_ID>>.env

    # export TO_DO_LIST_USER_POOL_CLIENT_ID=`aws cognito-idp list-user-pool-clients --user-pool-id $TO_DO_LIST_USER_POOL_ID | jq -r '.UserPoolClients | .[0].ClientId'`
    # echo TO_DO_LIST_USER_POOL_CLIENT_ID=$TO_DO_LIST_USER_POOL_CLIENT_ID>>.env

    # export TO_DO_LIST_USER_POOL_ARN=`aws cognito-idp describe-user-pool --user-pool-id $TO_DO_LIST_USER_POOL_ID | jq -r '.UserPool.Arn'`
    # echo TO_DO_LIST_USER_POOL_ARN=$TO_DO_LIST_USER_POOL_ARN>>.env

    # export TO_DO_LIST_ID_POOL_ID=`aws cognito-identity list-identity-pools --max-results 1 | jq -r '.IdentityPools | .[0].IdentityPoolId'`
    # echo TO_DO_LIST_ID_POOL_ID=$TO_DO_LIST_ID_POOL_ID>>.env
    # echo '#<<'>>.env

    aws cognito-idp create-user-pool-domain --domain $TO_DO_LIST_COGNITO_DOMAIN_BASE --user-pool-id $TO_DO_LIST_USER_POOL_ID

    aws cognito-idp update-user-pool-client --user-pool-id $TO_DO_LIST_USER_POOL_ID --client-id $TO_DO_LIST_USER_POOL_CLIENT_ID\
     --supported-identity-providers "COGNITO"\
     --callback-urls "[\"https://s3-${TARGET_REGION}.amazonaws.com/${TO_DO_LIST_APPS_BUCKET}/index.html\"]"\
     --logout-urls "[\"https://s3-${TARGET_REGION}.amazonaws.com/${TO_DO_LIST_APPS_BUCKET}/index.html\"]"\
     --allowed-o-auth-flows "implicit"\
     --allowed-o-auth-scopes "email" "openid" "aws.cognito.signin.user.admin"\
     --allowed-o-auth-flows-user-pool-client
  ;;
  teardown)
    aws cognito-idp delete-user-pool-domain --domain $TO_DO_LIST_COGNITO_DOMAIN_BASE --user-pool-id $TO_DO_LIST_USER_POOL_ID
  ;;
  *)
    echo 'nope'
  ;;
esac
