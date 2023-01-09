from git import Repo
repo = Repo()
print(repo.untracked_files, 3)
changedFiles = [ item.a_path for item in repo.index.diff(None) ]
print(changedFiles,)


# from git import Repo
# # Suppose the current path is the root of the repository
# r = Repo('.')
# o = r.git.show('HEAD', name_only=True)
# diff = repo.git.diff('HEAD~1..HEAD', name_only=True)
# print(diff, 124)
# print(o)
# # print(dir(repo))
# print(repo.untracked_files, 11)
# print(repo.working_dir)
# python .git/hooks/post-commit.py
print('TEST######')

