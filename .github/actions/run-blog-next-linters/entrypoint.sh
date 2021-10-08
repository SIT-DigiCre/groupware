#!/bin/sh

set -e

# -------------
# Environments
# -------------

RUN=$1
WORKING_DIR=$2
SEND_COMMENT=$3
GITHUB_TOKEN=$4
GITHUB_PR_NUM=$5
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
run_yarn() {
    set +xe

    # including auto format
    # aggressive にすることで、すこしキツめにlintingする
    OUTPUT=$(sh -c "yarn $*" 2>&1)
    SUCCESS=$?

    # for debug
    # 調べたけどいい方法がなかったので, もっといい方法があったら修正してください
    echo "$ yarn $*"
    echo "${OUTPUT}"


    set -xe

    # exit successfully
    if [ ${SUCCESS} -eq 0 ]; then
	return
    fi

    if [ "${SEND_COMMENT}" = "true" ]; then
	COMMENT="## $* failed
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
set +x
run_yarn ${RUN}

if [ ${SUCCESS} -ne 0 ]; then
    echo "Check failed."
    echo "${COMMENT}"
    if [ "${SEND_COMMENT}" = "true" ]; then
	send_comment
    fi
fi

set -x
exit ${SUCCESS}
