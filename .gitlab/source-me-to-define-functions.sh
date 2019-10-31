
hello_world_function () {
  echo "Hello world! (from hello_world_function)"
}

echo_some_vars () {
echo "CI........................................... $CI"
echo "CI_BUILDS_DIR................................ $CI_BUILDS_DIR"
echo "CI_CONCURRENT_ID............................. $CI_CONCURRENT_ID"
echo "CI_CONCURRENT_PROJECT_ID..................... $CI_CONCURRENT_PROJECT_ID"
echo "CI_COMMIT_BEFORE_SHA......................... $CI_COMMIT_BEFORE_SHA"
echo "CI_COMMIT_REF_NAME........................... $CI_COMMIT_REF_NAME"
echo "CI_COMMIT_SHA................................ $CI_COMMIT_SHA"
echo "CI_JOB_ID.................................... $CI_JOB_ID"
echo "CI_JOB_NAME.................................. $CI_JOB_NAME"
echo "CI_JOB_STAGE................................. $CI_JOB_STAGE"
echo "CI_PROJECT_DIR............................... $CI_PROJECT_DIR"
echo "CI_PROJECT_ID................................ $CI_PROJECT_ID"
echo "CI_REPOSITORY_URL............................ $CI_REPOSITORY_URL"
echo "CI_RUNNER_EXECUTABLE_ARCH.................... $CI_RUNNER_EXECUTABLE_ARCH"
echo "CI_RUNNER_ID................................. $CI_RUNNER_ID"
echo "CI_RUNNER_REVISION........................... $CI_RUNNER_REVISION"
echo "CI_RUNNER_TAGS............................... $CI_RUNNER_TAGS"
echo "CI_RUNNER_VERSION............................ $CI_RUNNER_VERSION"
echo "CI_RUNNER_SHORT_TOKEN........................ $CI_RUNNER_SHORT_TOKEN"
echo "CI_SERVER.................................... $CI_SERVER"
echo "CI_SERVER_HOST............................... $CI_SERVER_HOST"
echo "CI_SERVER_NAME............................... $CI_SERVER_NAME"
echo "CI_SHARED_ENVIRONMENT........................ $CI_SHARED_ENVIRONMENT"
echo "GITLAB_CI.................................... $GITLAB_CI"
}