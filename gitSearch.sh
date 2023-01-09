#!/bin/bash

# Set the repository path

function get_branch() {
      git branch --no-color | grep -E '^\*' | awk '{print $2}' \
        || echo "default_value"
      # or
      # git symbolic-ref --short -q HEAD || echo "default_value";
}

# Change to the repository directory
cd "${pwd}"

# Get the list of changed files
branch_name=`get_branch`;
changed_files=$(git diff --stat --staged origin/"$branch_name")
# Check if there are any changed files
if [ -z "$changed_files" ]; then
  echo "No changed files."
else
  # Print the list of changed files
  echo "$changed_files"
fi