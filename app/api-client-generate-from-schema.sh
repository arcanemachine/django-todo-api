#!/bin/bash

# examples
# - from schema.yml:
#   openapi-generator-cli generate -i schema.yml -g typescript-fetch -o ./api-client/
# - from URL:
#   openapi-generator-cli generate -i http://localhost:8000/api/schema/ -g typescript-fetch -o ./api-client/

if [ "$1" != "" ]; then
  client_language="$1"
else
  client_language="typescript-fetch"
fi
echo "Generating API client for language: '$client_language'"


openapi-generator-cli generate -i schema.yml -g $client_language -o ./api-client/
