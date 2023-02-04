# Set the repository path

function get_branch() {
      git branch --no-color | grep -E '^\*' | awk '{print $2}' \
        || echo "default_value"
      # or
      # git symbolic-ref --short -q HEAD || echo "default_value";
}

# Change to the repository directory
cd "${pwd}"

echo "NO CHANGED FILED"
# Get the list of changed files
branch_name=`get_branch`;
changed_files=$(git diff --name-only --staged origin/"$branch_name")
# Check if there are any changed files
if [ -z "$changed_files" ]; then
  echo "No changed files."
else
  # Print the list of changed files
  # echo "$changed_files"

  # Define endpoint URL
  endpoint="https://example.com/upload"

  for file in $changed_files; do
    # Send each changed file to endpoint
    echo "$file"
    echo "$endpoint"
    # curl -X POST -F "file=@$file" $endpoint
  done
fi