#!/bin/sh

set -e

# -------------
# Environments
# -------------

RUN=$1
WORKING_DIR=$2
SEND_COMMENT=$3
GITHUB_TOKEN=$4
COMMENT=""
SUCCESS=0

# if not set, assign default value
if [ "$2" = "" ]; then
    WORKING_DIR="."
fi
if [ "$3" = "" ]; then
    SEND_COMMENT="true"
fi

cd ${WORKING_DIR}

# ------------
# Functions
# ------------

# send_comment sends ${COMMENT} to pull request
# this function uses ${GITHUB_TOKEN}, ${COMMENT} and ${GITHUB_EVENT_PATH}
send_comment() {
    PAYLOAD=$(echo '{}' | jq --arg body "${COMMENT}" '.body = $body')
    COMMENTS_URL=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)
    curl -s -S -H "Authorization: token ${GITHUB_TOKEN}" --header "Content-Type: application/json" --data "${PAYLOAD}" "${COMMENTS_URL}" > /dev/null
}


# run_autopep8 for static analysis
run_autopep8() {
    set +e

    # including auto format
    OUTPUT=$(sh -c "autopep8 -r -i *.py $*" 2>&1)
    SUCCESS=$?

    set -e

    # exit successfully
    if [ ${SUCCESS} -eq 0 ]; then
	return
    fi

    if [ "${SEND_COMMENT}" = "true" ]; then
	COMMENT="## autopep8 failed
<details><summary>Show Detail</summary>

\`\`\`
$(echo "${OUTPUT}" | sed -e '$d')
\`\`\`
</details>

"
    fi
}


# run_flake8 for static analysis
run_flake8() {
    set +e

    OUTPUT=$(sh -c "flake8 . $*" 2>&1)
    SUCCESS=$?

    set -e

    # exit successfully
    if [ ${SUCCESS} -eq 0 ]; then
	return
    fi

    if [ "${SEND_COMMENT}" = "true" ]; then
	COMMENT="## flake8 failed
<details><summary>Show Detail</summary>

\`\`\`
$(echo "${OUTPUT}" | sed -e '$d')
\`\`\`
</details>

"
    fi
}


# -------------
# Main
# ------------
case ${RUN} in
    "autopep8" )
	run_autopep8
	;;
    "flake8" )
	run_flake8
	;;
    * )
	echo "Invalid command."
	exit 1
esac

if [ ${SUCCESS} -ne 0 ]; then
    echo "Check failed."
    echo "${COMMENT}"
    if [ "${SEND_COMMENT}" = "true" ]; then
	send_comment
    fi
fi

exit ${SUCCESS}