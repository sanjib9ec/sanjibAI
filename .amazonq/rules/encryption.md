Do a review of any  *.py for any CRITICAL or HIGH issues.


# Server Side Encryption
Description: redsift or S3 data missing server side encryption
Rule: Flag MEDIUM severity if found.


# No Hardcoding of environment
Description: Any bucket name containing which is not parameterized.e.g name contains dev/test/prod/prd instead of {env}
Rule: Flag HIGH severity if found.

# Configurations or Config should be in separate YML file
Description: any config such as s3 bucket name ,path key should be in separate .yml or .YAMl file
Rule: Flag HIGH severity if found.

