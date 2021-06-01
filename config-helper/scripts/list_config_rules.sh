#!/bin/bash
# set env var
. $CONFIG_HELPER_HOME/scripts/env.sh

PROGRAM=$(basename $0)

usage() {
  echo "Usage: $PROGRAM [config.json]"
  echo "If parameter exists, use specified manifest.  Otherise, use config.json in current working directory."
}

usage_and_exit()
{
    usage
    exit $1
}

error()
{
    echo "$@" 1>&2
    usage_and_exit 1
}


if [ $# -eq 0 ]; then
  config_json="config.json"
else
  config_json=$1
fi

if [ ! -f $config_json ]; then
  error "$config_json file does not exist."
fi

# list config rules that have been deployed
echo "[CMD] python3 $CONFIG_HELPER_HOME/scripts/list_config_rules.py $config_json"
python3 $CONFIG_HELPER_HOME/scripts/list_config_rules.py $config_json

