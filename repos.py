import subprocess as s
import os
import platform
import sys
import keyring
from keyrings.alt.file import PlaintextKeyring
import pwinput
import requests
import json

def get_shared_token():
    if platform.system() == "Windows":
        directory = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'RepoM')
    else:
        directory = '/var/lib/RepoM'
    
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except PermissionError:
            directory = os.path.expanduser("~/.repom")
            os.makedirs(directory, exist_ok=True)

    kr = PlaintextKeyring()
    kr.file_path = os.path.join(directory, "st.cfg")
    keyring.set_keyring(kr)

    token = keyring.get_password("RepoM", "df")
    
    if token is None:
        token = pwinput.pwinput("Enter GitHub Token: ", mask=".")
        keyring.set_password("RepoM", "df", token)
        if platform.system() != "Windows":
            os.chmod(kr.file_path, 0o600)
            
    return token

def main():
    try:
        if len(sys.argv) == 1:
            print("RepoManagement Wrapper for git and gh\nUsage: repom --<MyCommand>")
            return

        args = sys.argv[1:]
        
        if "--help" in args:
            print("Help screen called, commands:"
                  "\n--help: prints this help screen"
                  "\n--version: Prints version info"
                  "\n--makerepo <Name>: Create repo on GitHub"
                  "\n--initrepo: Runs git init"
                  "\n--delete <User> <Name>: Delete repo on GitHub"
                  "\n--setorigin <URLToRepo>: Sets git origin to the URL recieved."
                  "\n--pushdata <branch>: Pushes to origin"
                  "\n--pulldata <branch>: Pulls from origin"
                  "\n--addfile <filename>: Adds file name to get commited to"
                  "\n--commit <\"NameOfCommit\">: Adds a commit using the name given as the argument"
                  "\n--makebranch <User> <Repo> <branchname>: Creates a remote branch"
                  "\n--cleartoken: Clears the stored GitHub token")
            return

        if "--version" in args:
            print("RepoManagement 1.0.0"
            "\nCopyright (C) 2026 Alan"
            "\nLicense GPLv3+: GNU GPL version 3 or later <https://gnu.org>."
            "\nThis is free software: you are free to change and redistribute it."
            "\nThere is NO WARRANTY, to the extent permitted by law.")
            return

        if "--cleartoken" in args:
            directory = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'RepoM') if platform.system() == "Windows" else '/var/lib/RepoM'
            kr = PlaintextKeyring()
            kr.file_path = os.path.join(directory, "st.cfg")
            keyring.set_keyring(kr)
            try:
                keyring.delete_password("RepoM", "df")
                print("Token cleared successfully.")
            except:
                print("No token found to clear.")
            return

        token = get_shared_token()
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RepoM-CLI-App"
        }

        if "--makerepo" in args:
            repo_name = args[args.index("--makerepo") + 1]
            resp = requests.post("https://api.github.com/user/repos", json={"name": repo_name}, headers=headers)
            if resp.status_code == 201:
                repo_url = resp.json().get("html_url")
                print(f"Repository created: {repo_url}")
            else:
                print(f"GitHub Error {resp.status_code}: {resp.text}")

        if "--delete" in args:
            idx = args.index("--delete")
            user, repo = args[idx + 1], args[idx + 2]
            resp = requests.delete(f"https://api.github.com/repos/{user}/{repo}", headers=headers)
            if resp.status_code == 204:
                print(f"Successfully deleted: {user}/{repo}")
            else:
                print(f"Delete failed {resp.status_code}: {resp.text}")

        if "--initrepo" in args:
            s.run(["git", "init"])
            s.run(["git", "branch", "-M", "main"])
            
        if "--setorigin" in args:
            url = args[args.index("--setorigin") + 1]
            s.run(["git", "remote", "add", "origin", url])
            print(f"Origin set to: {url}")

        if "--addfile" in args:
            filename = args[args.index("--addfile") + 1]
            s.run(["git", "add", filename])
            print(f"Added: {filename}")
            
        if "--commit" in args:
            commitname = args[args.index("--commit") + 1]
            s.run(["git", "commit", "-m", commitname])
            print(f"Committed: {commitname}")
            
        if "--pushdata" in args:
            branchname = args[args.index("--pushdata") + 1]
            s.run(["git", "push", "origin", branchname])
            
        if "--pulldata" in args:
            branchname = args[args.index("--pulldata") + 1]
            s.run(["git", "pull", "origin", branchname])

        if "--makebranch" in args:
            idx = args.index("--makebranch")
            user, repo, new_branch = args[idx + 1], args[idx + 2], args[idx + 3]
            ref_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/git/refs/heads/main", headers=headers)
            if ref_resp.status_code == 200:
                sha = ref_resp.json()['object']['sha']
                create_resp = requests.post(
                    f"https://api.github.com/repos/{user}/{repo}/git/refs", 
                    json={"ref": f"refs/heads/{new_branch}", "sha": sha}, 
                    headers=headers
                )
                if create_resp.status_code == 201:
                    print(f"Remote branch {new_branch} created.")
                else:
                    print(f"Error {create_resp.status_code}: {create_resp.text}")
            else:
                print(f"Error {ref_resp.status_code}: {ref_resp.text}")

    except (IndexError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == "__main__":
    main()