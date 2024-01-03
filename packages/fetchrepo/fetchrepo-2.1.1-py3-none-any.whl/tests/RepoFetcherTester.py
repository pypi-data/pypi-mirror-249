from FetchRepo.RepoFetcher import harvest_github_repo

repo_link = "https://github.com/testvagrant/playwrite-e2e-framework"
access_token = "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"
code = harvest_github_repo(repo_link,branch="main",access_token=access_token)
print(code)