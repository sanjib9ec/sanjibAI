Do a review of the files in *.py for any CRITICAL or HIGH issues.
Put any review comments in seperate json files under the '.amazonq/review/' directory the json files must be in the format

{
  "filepath": <relative path to the file>,
  "comment": <The review comment>,
  "suggested_change": <the suggested code change>,
  "start_line": <the start line of the suggestion>,
  "end_line": <the end line of the suggestion>
}

# Server Side Encryption
Description: redsift or S3 data missing server side encryption
Rule: Flag every TODO as MEDIUM severity.


# No Hardcoding of environment
Description: Any bucket name containing which is not parameterized.e.g name contains dev/test/prod/prd instead of {env}
Rule: Flag every TODO as HIGH severity.

