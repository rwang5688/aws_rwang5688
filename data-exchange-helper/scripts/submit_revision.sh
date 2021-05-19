#!/bin/bash
# set env var
. $DATA_EXCHANGE_HELPER_HOME/scripts/env.sh

PROGRAM=$(basename $0)

usage() {
  echo "Usage: $PROGRAM [revision.manifest]"
  echo "If parameter exists, use specified manifest.  Otherise, use revision.manifest in current working directory."
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
  revision_manifest="revision.manifest"
else
  revision_manifest=$1
fi

if [ ! -f $revision_manifest ]; then
  error "$revision_manifest file does not exist."
fi

# submit revision with revision manifest
echo "[CMD] python3 $DATA_EXCHANGE_HELPER_HOME/scripts/submit_revision.py $revision_manifest"
python3 $DATA_EXCHANGE_HELPER_HOME/scripts/submit_revision.py $revision_manifest

