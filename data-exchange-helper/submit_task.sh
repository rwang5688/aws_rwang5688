#!/bin/bash
# set env vars
. $SUBMIT_TASK/env.sh

PROGRAM=$(basename $0)

usage() {
  echo "Usage: $PROGRAM [xcal-task.conf]"
  echo "Note: if no parameter provided, use xcal-task.conf file in current work path. Otherwise, use the file specified by the parameter"
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
  task_conf="xcal-task.conf"
else
  task_conf=$1
fi

if [ ! -f $task_conf ]; then
  error "$task_conf file does not exist"
fi

# submit task based on task_id1_context_user_id.json
# read ./xcalagent contents: fileinfo.json, preprocess.tar.gz, source_code.zip
echo "[CMD] python3 $SUBMIT_TASK/submit_task.py $task_conf"
python3 $SUBMIT_TASK/submit_task.py $task_conf

