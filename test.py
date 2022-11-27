from git import Repo
repo = Repo()
changedFiles = [ item.a_path for item in repo.index.diff(None) ]
print(changedFiles, repo)