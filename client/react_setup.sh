#!/bin/bash

echo "Waiting for backend..."
while ! nc -z backend 8000; do sleep 1; done;
echo "Backend up."
npm start

