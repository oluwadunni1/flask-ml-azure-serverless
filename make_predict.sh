#!/usr/bin/env bash

PORT=5000
echo "Port: $PORT"

# POST method predict
curl -d '{
   "SquareFeet": [2500],
   "Bedrooms": [3],
   "Bathrooms": [2],
   "YearBuilt": [2015],
   "Neighborhood": ["Rural"]
}' -H "Content-Type: application/json" -X POST http://localhost:$PORT/predict
