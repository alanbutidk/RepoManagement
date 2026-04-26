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
                  "\n--makerelease <User> <Repo> <Executable/Directory/.> -tag <v1.0.0>: Creates a GitHub release using RELEASE.md in the given path"
                  "\n--listrepos <User>: Lists all repos for a user"
                  "\n--listbranches <User> <Repo>: Lists all branches in a repo"
                  "\n--makePR <User> <Repo> <head> <base> <Title>: Opens a pull request from head into base"
                  "\n--clonerepo <User> <Repo>: Clones a repo by user and name"
                  "\n--GenToken <TokenName>: Generates a new GitHub token (requires token with admin:org scope)"
                  "\n--getrelease <User> <Repo> <Tag> <OSType> <Arch>: Downloads a release asset matching OS and architecture"
                  "\n--getrelease <User> <Repo> <Tag> <Filename.ext>: Downloads a specific named asset from a release"
                  "\n--getrelease <User> <Repo> Source-<.zip/.gz>: Downloads the release source archive in the given format"
                  "\n--deletefile <User> <Repo> <Branch> <Filename.Format>: Deletes a file from a branch"
                  "\n--deleterelease <User> <Repo> <Tag> <Filename.Format> [OSName] [Arch]: Deletes a release asset by name, optionally filtered by OS and arch"
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

        if "--makerelease" in args:
            idx = args.index("--makerelease")
            user, repo, target = args[idx + 1], args[idx + 2], args[idx + 3]

            tag = "v1.0.0"
            if "-tag" in args:
                tag = args[args.index("-tag") + 1]

            if target == ".":
                search_dir = os.getcwd()
            elif os.path.isdir(target):
                search_dir = target
            else:
                search_dir = os.path.dirname(os.path.abspath(target))

            release_md = os.path.join(search_dir, "RELEASE.md")
            if not os.path.exists(release_md):
                print(f"Error: RELEASE.md not found in {search_dir}")
            else:
                with open(release_md, "r") as f:
                    release_body = f.read()

                release_resp = requests.post(
                    f"https://api.github.com/repos/{user}/{repo}/releases",
                    json={"tag_name": tag, "name": tag, "body": release_body, "draft": False, "prerelease": False},
                    headers=headers
                )

                if release_resp.status_code == 201:
                    release_data = release_resp.json()
                    upload_url = release_data["upload_url"].replace("{?name,label}", "")
                    print(f"Release {tag} created: {release_data['html_url']}")

                    if os.path.isfile(target):
                        exe_path = target
                    else:
                        exe_path = None
                        for f_name in os.listdir(search_dir):
                            f_path = os.path.join(search_dir, f_name)
                            if os.path.isfile(f_path) and os.access(f_path, os.X_OK) and f_name != "RELEASE.md":
                                exe_path = f_path
                                break

                    if exe_path:
                        exe_name = os.path.basename(exe_path)
                        upload_headers = {**headers, "Content-Type": "application/octet-stream"}
                        with open(exe_path, "rb") as ef:
                            up_resp = requests.post(
                                f"{upload_url}?name={exe_name}",
                                headers=upload_headers,
                                data=ef
                            )
                        if up_resp.status_code == 201:
                            print(f"Uploaded asset: {exe_name}")
                        else:
                            print(f"Asset upload failed {up_resp.status_code}: {up_resp.text}")
                    else:
                        print("No executable asset found to upload.")
                else:
                    print(f"Release failed {release_resp.status_code}: {release_resp.text}")

        if "--listrepos" in args:
            idx = args.index("--listrepos")
            user = args[idx + 1]
            page = 1
            all_repos = []
            while True:
                resp = requests.get(
                    f"https://api.github.com/users/{user}/repos",
                    params={"per_page": 100, "page": page},
                    headers=headers
                )
                if resp.status_code == 200:
                    batch = resp.json()
                    if not batch:
                        break
                    all_repos.extend(batch)
                    page += 1
                else:
                    print(f"Error {resp.status_code}: {resp.text}")
                    break
            if all_repos:
                print(f"Repositories for {user} ({len(all_repos)} total):")
                for r in all_repos:
                    visibility = "private" if r.get("private") else "public"
                    print(f"  {r['name']} [{visibility}] - {r.get('description') or 'No description'}")
            else:
                print(f"No repositories found for {user}.")

        if "--listbranches" in args:
            idx = args.index("--listbranches")
            user, repo = args[idx + 1], args[idx + 2]
            resp = requests.get(
                f"https://api.github.com/repos/{user}/{repo}/branches",
                params={"per_page": 100},
                headers=headers
            )
            if resp.status_code == 200:
                branches = resp.json()
                print(f"Branches in {user}/{repo} ({len(branches)} total):")
                for b in branches:
                    print(f"  {b['name']}")
            else:
                print(f"Error {resp.status_code}: {resp.text}")

        if "--makePR" in args:
            idx = args.index("--makePR")
            user, repo, head, base, title = args[idx + 1], args[idx + 2], args[idx + 3], args[idx + 4], args[idx + 5]
            resp = requests.post(
                f"https://api.github.com/repos/{user}/{repo}/pulls",
                json={"title": title, "head": head, "base": base},
                headers=headers
            )
            if resp.status_code == 201:
                pr = resp.json()
                print(f"Pull request created: {pr['html_url']}")
            else:
                print(f"PR failed {resp.status_code}: {resp.text}")

        if "--clonerepo" in args:
            idx = args.index("--clonerepo")
            user, repo = args[idx + 1], args[idx + 2]
            clone_url = f"https://github.com/{user}/{repo}.git"
            result = s.run(["git", "clone", clone_url])
            if result.returncode == 0:
                print(f"Cloned {user}/{repo} successfully.")
            else:
                print(f"Clone failed for {user}/{repo}.")

        if "--GenToken" in args:
            idx = args.index("--GenToken")
            token_name = args[idx + 1]
            resp = requests.post(
                "https://api.github.com/user/tokens",
                json={
                    "name": token_name,
                    "scopes": ["repo", "read:org", "workflow"]
                },
                headers=headers
            )
            if resp.status_code == 201:
                new_token = resp.json().get("token")
                print(f"New token generated: {new_token}")
                print("Save this token now, it will not be shown again.")
            elif resp.status_code == 404:
                print("Token generation not supported via this API endpoint. Use GitHub Settings > Developer settings > Personal access tokens.")
            elif resp.status_code == 403:
                print("Permission denied. Your current token does not have the scope to generate new tokens.")
            else:
                print(f"GenToken failed {resp.status_code}: {resp.text}")

        if "--getrelease" in args:
            idx = args.index("--getrelease")
            user, repo = args[idx + 1], args[idx + 2]
            fourth_arg = args[idx + 3]

            if fourth_arg.startswith("Source-"):
                ext = fourth_arg.split("Source-")[1].lower()
                tag = args[idx + 4] if len(args) > idx + 4 and not args[idx + 4].startswith("--") else "latest"

                if tag == "latest":
                    rel_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/latest", headers=headers)
                else:
                    rel_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/tags/{tag}", headers=headers)

                if rel_resp.status_code != 200:
                    print(f"Release fetch failed {rel_resp.status_code}: {rel_resp.text}")
                else:
                    rel_data = rel_resp.json()
                    actual_tag = rel_data["tag_name"]
                    if ext in (".zip", "zip"):
                        download_url = rel_data.get("zipball_url")
                        out_file = f"{repo}-{actual_tag}.zip"
                    elif ext in (".gz", "tar.gz", "gz"):
                        download_url = rel_data.get("tarball_url")
                        out_file = f"{repo}-{actual_tag}.tar.gz"
                    else:
                        print(f"Unknown source format: {ext}. Use .zip or .gz")
                        download_url = None

                    if download_url:
                        print(f"Downloading source {ext} for {user}/{repo} {actual_tag}...")
                        dl = requests.get(download_url, headers=headers, stream=True, allow_redirects=True)
                        with open(out_file, "wb") as f:
                            for chunk in dl.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Saved: {out_file}")

            elif len(args) > idx + 4 and '.' in args[idx + 4] and not args[idx + 4].startswith("--"):
                tag = fourth_arg
                filename = args[idx + 4]

                if tag == "latest":
                    rel_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/latest", headers=headers)
                else:
                    rel_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/tags/{tag}", headers=headers)

                if rel_resp.status_code != 200:
                    print(f"Release fetch failed {rel_resp.status_code}: {rel_resp.text}")
                else:
                    rel_data = rel_resp.json()
                    actual_tag = rel_data["tag_name"]
                    assets = rel_data.get("assets", [])
                    matched = next((a for a in assets if a["name"].lower() == filename.lower()), None)
                    if not matched:
                        print(f"Asset '{filename}' not found in release {actual_tag}.")
                        print("Available assets:")
                        for asset in assets:
                            print(f"  {asset['name']}")
                    else:
                        out_file = matched["name"]
                        download_url = matched["browser_download_url"]
                        print(f"Downloading {out_file} from {user}/{repo} {actual_tag}...")
                        dl = requests.get(download_url, headers=headers, stream=True, allow_redirects=True)
                        with open(out_file, "wb") as f:
                            for chunk in dl.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Saved: {out_file}")

            else:
                tag, os_type, arch = fourth_arg, args[idx + 4], args[idx + 5]

                os_aliases = {
                    "windows": ["windows", "win", "win32", "win64"],
                    "linux":   ["linux"],
                    "macos":   ["macos", "darwin", "osx", "mac"],
                }
                arch_aliases = {
                    "x86_64": ["x86_64", "amd64", "x64"],
                    "x86":    ["x86", "i386", "i686", "32bit"],
                    "arm64":  ["arm64", "aarch64"],
                    "arm":    ["arm", "armv7"],
                }

                os_lower = os_type.lower()
                arch_lower = arch.lower()

                matched_os_terms = next((v for v in os_aliases.values() if os_lower in v), [os_lower])
                matched_arch_terms = next((v for v in arch_aliases.values() if arch_lower in v), [arch_lower])

                if tag == "latest":
                    rel_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/latest", headers=headers)
                else:
                    rel_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/releases/tags/{tag}", headers=headers)

                if rel_resp.status_code != 200:
                    print(f"Release fetch failed {rel_resp.status_code}: {rel_resp.text}")
                else:
                    rel_data = rel_resp.json()
                    actual_tag = rel_data["tag_name"]
                    assets = rel_data.get("assets", [])

                    matched = None
                    for asset in assets:
                        name_lower = asset["name"].lower()
                        os_match = any(term in name_lower for term in matched_os_terms)
                        arch_match = any(term in name_lower for term in matched_arch_terms)
                        if os_match and arch_match:
                            matched = asset
                            break

                    if not matched:
                        print(f"No asset found matching OS '{os_type}' and arch '{arch}' in release {actual_tag}.")
                        print("Available assets:")
                        for asset in assets:
                            print(f"  {asset['name']}")
                    else:
                        out_file = matched["name"]
                        download_url = matched["browser_download_url"]
                        print(f"Downloading {out_file} from {user}/{repo} {actual_tag}...")
                        dl = requests.get(download_url, headers=headers, stream=True, allow_redirects=True)
                        with open(out_file, "wb") as f:
                            for chunk in dl.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Saved: {out_file}")

        if "--deletefile" in args:
            idx = args.index("--deletefile")
            user, repo, branch, filename = args[idx + 1], args[idx + 2], args[idx + 3], args[idx + 4]

            file_resp = requests.get(
                f"https://api.github.com/repos/{user}/{repo}/contents/{filename}",
                params={"ref": branch},
                headers=headers
            )
            if file_resp.status_code != 200:
                print(f"File '{filename}' not found on branch '{branch}': {file_resp.status_code}")
            else:
                sha = file_resp.json()["sha"]
                del_resp = requests.delete(
                    f"https://api.github.com/repos/{user}/{repo}/contents/{filename}",
                    json={"message": f"Delete {filename}", "sha": sha, "branch": branch},
                    headers=headers
                )
                if del_resp.status_code == 200:
                    print(f"Deleted '{filename}' from {user}/{repo} on branch '{branch}'.")
                else:
                    print(f"Delete failed {del_resp.status_code}: {del_resp.text}")

        if "--deleterelease" in args:
            idx = args.index("--deleterelease")
            user, repo, tag = args[idx + 1], args[idx + 2], args[idx + 3]
            filename = args[idx + 4] if len(args) > idx + 4 else None
            os_filter = args[idx + 5].lower() if len(args) > idx + 5 else None
            arch_filter = args[idx + 6].lower() if len(args) > idx + 6 else None

            rel_resp = requests.get(
                f"https://api.github.com/repos/{user}/{repo}/releases/tags/{tag}",
                headers=headers
            )
            if rel_resp.status_code != 200:
                print(f"Release '{tag}' not found: {rel_resp.status_code}")
            else:
                assets = rel_resp.json().get("assets", [])

                if filename:
                    base_name = filename.lower()
                    candidates = [a for a in assets if a["name"].lower() == base_name]

                    if not candidates:
                        candidates = [a for a in assets if base_name in a["name"].lower()]

                    if os_filter:
                        os_aliases = {
                            "windows": ["windows", "win", "win32", "win64"],
                            "linux":   ["linux"],
                            "macos":   ["macos", "darwin", "osx", "mac"],
                        }
                        os_terms = next((v for v in os_aliases.values() if os_filter in v), [os_filter])
                        candidates = [a for a in candidates if any(t in a["name"].lower() for t in os_terms)]

                    if arch_filter:
                        arch_aliases = {
                            "x86_64": ["x86_64", "amd64", "x64"],
                            "x86":    ["x86", "i386", "i686", "32bit"],
                            "arm64":  ["arm64", "aarch64"],
                            "arm":    ["arm", "armv7"],
                        }
                        arch_terms = next((v for v in arch_aliases.values() if arch_filter in v), [arch_filter])
                        candidates = [a for a in candidates if any(t in a["name"].lower() for t in arch_terms)]
                else:
                    candidates = assets

                if not candidates:
                    print(f"No matching assets found in release '{tag}'.")
                    print("Available assets:")
                    for a in assets:
                        print(f"  {a['name']}")
                elif len(candidates) > 1:
                    print(f"Multiple assets matched — please be more specific:")
                    for a in candidates:
                        print(f"  {a['name']}")
                else:
                    asset = candidates[0]
                    del_resp = requests.delete(
                        f"https://api.github.com/repos/{user}/{repo}/releases/assets/{asset['id']}",
                        headers=headers
                    )
                    if del_resp.status_code == 204:
                        print(f"Deleted asset '{asset['name']}' from release '{tag}'.")
                    else:
                        print(f"Asset delete failed {del_resp.status_code}: {del_resp.text}")

    except (IndexError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == "__main__":
    main()