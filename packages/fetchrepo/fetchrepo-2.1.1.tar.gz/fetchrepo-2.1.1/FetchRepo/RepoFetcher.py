import os
import requests
import tarfile
import tempfile
from io import BytesIO
import json

def _download_and_extract_repo(https_link, branch=None, headers=None):
    response = requests.get(https_link, headers=headers)
    if response.status_code == 200:
        return response.content if response.content else None
    print('Failed to download the repository')
    return None

def _is_binary(data):
    binary_threshold = 0.2
    if data:
        non_ascii_ratio = sum(1 for char in data if char < 32 or char > 127) / len(data)
        return non_ascii_ratio > binary_threshold
    return False

def _read_ignore_files(file_path):
    return [
        ".gitignore", "README.md", ".DS_Store", "package-lock.json","assets/","asset/",
        "image/","img/","pictures/","pics/","picture/","pic/",
        "package.json", ".github/", "images/", ".prettierrc", ".vscode/"
        "node_modules/", "tsconfig.json", "LICENSE", "build/","dist/","lib/",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", 
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv",  
        ".mp3", ".wav", ".ogg", ".flac", ".aac",
    ]

def _exclude_files(file_path, ignore_files):
    for excluded_file in ignore_files:
        if excluded_file.lower() in file_path.lower():
            return True
    return False

def _convert_to_json(repo_content, root_dir, ignore_files):
    result = []
    if not repo_content:
        return result

    with tempfile.TemporaryDirectory() as temp_dir, \
         tarfile.open(fileobj=BytesIO(repo_content), mode="r:gz") as tar:
        tar.extractall(temp_dir)
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), temp_dir)

                if _exclude_files(file_path, ignore_files):
                    continue

                with open(os.path.join(root, file), 'rb') as f:
                    file_content = f.read()
                    if _is_binary(file_content):
                        continue
                    file_content = file_content.decode('utf-8', errors='replace')

                formatted_path = os.path.join(root_dir, file_path).replace(os.path.sep, '/')
                formatted_content = _indent_code(file_content)
                file_info = {"file_path": formatted_path, "content": formatted_content}
                result.append(file_info)

    return result

def _indent_code(code):
    indented_code = '\n'.join(['    ' + line for line in code.splitlines()])
    return indented_code

def _print_repo_content_json(repo_content, root_dir, ignore_files):
    json_structure = _convert_to_json(repo_content, root_dir, ignore_files)
    formatted_json = json.dumps(json_structure, indent=2, separators=(',', ': '), sort_keys=True)
    return formatted_json

def _get_github_repo_branches(repo_link, headers=None):
    owner, repo = repo_link.split("/")[-2:]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        branches = response.json()
        branch_names = [branch["name"] for branch in branches]
        print("Branches:", branch_names)
        return branch_names
    else:
        print(f"Failed to list branches. Status code: {response.status_code}")
        return None

def harvest_github_repo(repo_link, branch=None, access_token=None):
    headers = None
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}

    ignore_files = _read_ignore_files("ignore_files.txt")

    if not branch:
        branches = _get_github_repo_branches(repo_link, headers=headers)
        if not branches:
            print("Unable to fetch branches. Exiting.")
            return None

        branch = input("Select a branch from the list above: ")
        if branch not in branches:
            print("Invalid branch. Exiting.")
            return None

    repo_content = _download_and_extract_repo(f"{repo_link}/archive/{branch}.tar.gz", headers=headers)
    if not repo_content:
        print("Failed to download and extract repository content.")
        return None

    root_directory = os.getcwd()
    repo_content = _print_repo_content_json(repo_content, root_directory, ignore_files)

    return repo_content