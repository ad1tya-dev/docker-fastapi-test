#!/bin/bash

echo "Generating traffic to FastAPI..."

# Generate GET requests
for i in {1..100}; do
  curl -s http://localhost:8000/ > /dev/null &
  curl -s http://localhost:8000/users > /dev/null &
  sleep 0.1
done

# Add some users
echo "Adding users..."
for i in {1..10}; do
  curl -s -X POST http://localhost:8000/users \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"User$i\", \"last_name\": \"Test\", \"age\": $((20 + i)), \"email\": \"user$i@test.com\"}" > /dev/null
  sleep 0.5
done

# More GET requests
for i in {1..50}; do
  curl -s http://localhost:8000/users > /dev/null &
  sleep 0.2
done

wait
echo "Traffic generation complete!"
