#!/usr/bin/env bash

echo "Testing Azure App..."

curl -X POST https://flask-ml-dunni-2026.azurewebsites.net/predict      -H "Content-Type: application/json"      -d '{
           "SquareFeet": [2500],
           "Bedrooms": [3],
           "Bathrooms": [2],
           "YearBuilt": [2015],
           "Neighborhood": ["Rural"]
         }'
