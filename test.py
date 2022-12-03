from git import Repo
repo = Repo()
changedFiles = [ item.a_path for item in repo.index.diff(None) ]
print(changedFiles,)
from git import Repo

# Suppose the current path is the root of the repository
r = Repo('.')
o = r.git.show('HEAD', pretty="", name_only=True)
print(o)
# print(dir(repo)s

print(repo.untracked_files, 11)
print(repo.working_dir)

# python .git/hooks/post-commit.py