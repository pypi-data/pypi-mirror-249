#!/bin/bash

: '
This script pulls the Takeoff Server Docker image locally.

It performs the following steps:
1. Pulls the specific Docker image (tytn/fabulinus:latest) from a public registry (e.g., Docker Hub).
2. Optionally, you can customize the image name and tag as needed.

Usage:
- Run the script to pull the Docker image locally.
'



docker pull tytn/fabulinus:latest

