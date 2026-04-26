import subprocess as s
import os
import platform
import sys
import keyring
from keyrings.alt.file import PlaintextKeyring
import pwinput
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
            if platform.system() == "Windows":
                directory = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'RepoM')
            else:
                directory = '/var/lib/RepoM'
            kr = PlaintextKeyring()
            kr.file_path = os.path.join(directory, "st.cfg")
            if not os.path.exists(kr.file_path):
                directory = os.path.expanduser("~/.repom")
                kr.file_path = os.path.join(directory, "st.cfg")
            keyring.set_keyring(kr)
            try:
                keyring.delete_password("RepoM", "df")
                print("Token cleared successfully.")
            except:
                print("No token found to clear.")
            return

        if "--makerepo" in args:
            token = get_shared_token()
            repo_name = args[args.index("--makerepo") + 1]
            cmd = [
                "curl", "-s", "-X", "POST",
                "-H", f"Authorization: token {token}",
                "-d", json.dumps({"name": repo_name}),
                "https://api.github.com/user/repos"
            ]
            result = s.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                data = json.loads(result.stdout)
                repo_url = data.get("html_url")
                if repo_url:
                    print(f"Repository created: {repo_url}")
                    if "--set_asorigin" in args:
                        s.run(["git", "remote", "add", "origin", repo_url])
                        s.run(["git", "branch", "-M", "main"])
                        print(f"Origin set to: {repo_url}")
                else:
                    print(f"GitHub Error: {data.get('message', 'Check your token scopes.')}")
            else:
                print("Error: No response from GitHub. Verify your token and connection.")

        if "--delete" in args:
            token = get_shared_token()
            idx = args.index("--delete")
            user, repo = args[idx + 1], args[idx + 2]
            cmd = [
                "curl", "-s", "-X", "DELETE",
                "-H", f"Authorization: token {token}",
                f"https://github.com{user}/{repo}"
            ]
            s.run(cmd)
            print(f"Request sent to delete: {user}/{repo}")

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
            print(f"Added: {filename} to commits")
            
        if "--commit" in args:
            commitname = args[args.index("--commit") + 1]
            s.run(["git", "commit", "-m", commitname])
            print(f"Commit added with name: {commitname}")
            
        if "--pushdata" in args:
            branchname = args[args.index("--pushdata") + 1]
            s.run(["git", "push", "origin", branchname])
            print(f"Pushed data to branch: {branchname}")
            
        if "--pulldata" in args:
            branchname = args[args.index("--pulldata") + 1]
            s.run(["git", "pull", "origin", branchname])
            print(f"Pulled data from branch: {branchname}")

        if "--makebranch" in args:
            token = get_shared_token()
            idx = args.index("--makebranch")
            user, repo, new_branch = args[idx + 1], args[idx + 2], args[idx + 3]
            get_ref_cmd = ["curl", "-s", "-L", "-H", f"Authorization: token {token}", f"https://github.com{user}/{repo}/git/refs/heads/main"]
            resp = s.run(get_ref_cmd, capture_output=True, text=True)
            if resp.stdout.strip():
                ref_data = json.loads(resp.stdout)
                if 'object' in ref_data:
                    sha = ref_data['object']['sha']
                    create_cmd = [
                        "curl", "-s", "-X", "POST",
                        "-H", f"Authorization: token {token}",
                        "-d", json.dumps({"ref": f"refs/heads/{new_branch}", "sha": sha}),
                        f"https://github.com{user}/{repo}/git/refs"
                    ]
                    s.run(create_cmd)
                    print(f"Remote branch {new_branch} created.")
                else:
                    print(f"Error: {ref_data.get('message', 'Base branch main not found.')}")

    except IndexError:
        print("Error: Missing arguments for the command.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
