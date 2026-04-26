import subprocess
import os
import platform
import sys
import keyring
from keyrings.alt.file import PlaintextKeyring
import pwinput

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
        token = pwinput.pwinput("Enter GitHub Token: ", mask="*")
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
                  "\n--pushdata: Pushes to origin"
                  "\n--pulldata: Pulls from origin"
                  "\n--addfile <filename>: Adds file name to get commited to"
                  "\n--commit <\"NameOfCommit\">: Adds a commit using the name given as the argument")
            return

        if "--version" in args:
            print("RepoManagement 1.0.0\nCopyright (C) 2026 Alan\nLicense GPLv3+")
            return

        if "--makerepo" in args:
            token = get_shared_token()
            repo_name = args[args.index("--makerepo") + 1]
            cmd = [
                "curl", "-s", "-X", "POST",
                "-H", f"Authorization: token {token}",
                "-d", f'{{"name": "{repo_name}"}}',
                "https://github.com"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL)
            print(f"Request sent to create: {repo_name}")

        if "--delete" in args:
            token = get_shared_token()
            idx = args.index("--delete")
            user, repo = args[idx + 1], args[idx + 2]
            cmd = [
                "curl", "-s", "-X", "DELETE",
                "-H", f"Authorization: token {token}",
                f"https://github.com{user}/{repo}"
            ]
            subprocess.run(cmd)
            print(f"Request sent to delete: {user}/{repo}")

        if "--initrepo" in args:
            subprocess.run(["git", "init"])

    except IndexError:
        print("Error: Missing arguments for the command.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
