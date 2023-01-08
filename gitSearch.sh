#!/bin/bash

# Set the repository path


repo_path= "/Users/akindele214/Desktop/Dev/gitsecure"

# Change to the repository directory
cd "$repo_path"

# Get the list of changed files
changed_files=$(git diff --name-only)

# Check if there are any changed files
if [ -z "$changed_files" ]; then
  echo "No changed files."
else
  # Print the list of changed files
  echo "$changed_files"
fi