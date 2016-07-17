#!/bin/bash

#
#  Example:
#   ./update-wiki.sh prod master /somewhere/arcanist/bin/arc PHID-PROJ-ei42dbvlurp7h2ykspq6
#
#  Explanation:
#   req.       req.           req.              req.        opt.
#   executable wiki_namespace branch_to_analyze path_to_arc project_to_apply
#
#  First run only:
#   create .checkpoint file and put from the past (i.e. 2016-01-01)
#

set -e

CHECKPOINT_FILE=".checkpoint"
CONDUIT_URI="https://my.phabricator.com/"
DATE_NOW=`date +%Y-%m-%d`
SLUG="changelog/${1}/${DATE_NOW}"

DATE=$DATE_NOW
if [ -f "${CHECKPOINT_FILE}" ]; then
  DATE=`cat "${CHECKPOINT_FILE}"`
fi

if [ $DATE_NOW = $DATE ]; then
  echo "The last changelog generation was today"
  exit 0
fi

echo "Generating the changelog since ${DATE} until ${DATE_NOW}..."

OUTPUT=`python main.py --arc-executable=${3} changelog --branch=${2} --since=${DATE}`
JSON=`echo "${OUTPUT}" | python -c 'import sys, json; print(json.dumps(sys.stdin.read()))'`

echo "Checking the wiki page..."

METHOD="phriction.create"

echo "{\"slug\": \"${SLUG}\"}" \
  | $3 call-conduit --conduit-uri $CONDUIT_URI phriction.info 2>/dev/null \
  | grep "ERR-BAD-DOCUMENT" 1> /dev/null || METHOD="phriction.edit"

echo "Sending..."

echo "{\"slug\": \"${SLUG}\", \"title\": \"${DATE_NOW//-/ }\", \"content\": ${JSON}}" \
  | $3 call-conduit --conduit-uri $CONDUIT_URI $METHOD 1> /dev/null

echo $DATE_NOW > $CHECKPOINT_FILE
echo "Created: ${CONDUIT_URI}w/${SLUG}."

if [ ! -z "${4}" ]; then
  echo "Updating tags..."

  for id in `echo "${OUTPUT}" | grep 'T\([0-9]*\)' | cut -d'T' -f2 | awk '{print $1}'`; do
    echo "{\"objectIdentifier\": \"${id}\", \"transactions\": [{\"type\": \"projects.add\", \"value\": [\"${4}\"]}]}" \
      | $3 call-conduit --conduit-uri $CONDUIT_URI maniphest.edit 1> /dev/null
    echo -e " ${id}\c"
  done
fi

echo "\nDone."

exit 0
