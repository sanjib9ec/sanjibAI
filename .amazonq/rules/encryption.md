# No TODO comments
Description: Any line containing the string "TODO" should be flagged.
Rule: Flag every TODO as MEDIUM severity.


# No Hardcoding of environment
Description: Any bucket name containing which is not parameterized.e.g name contains dev/test/prod/prd instead of {env}
Rule: Flag every TODO as HIGH severity.