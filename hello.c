            if len(sys.argv) > 1:
                        if "--help" in sys.argv[1]:
                                    print("Help screen called, commands: "
                                    "\n--help: prints this help screen"
                                    "\n--version: Prints the version info"
                                    "\n--makerepo <RepoName>: makes a repo on github (for now)"
                                    "\n--initrepo: inits the repo for later uses."
                                    "\n--delete <Username> <RepoName>: deletes the repo on github (for now)"
                                    "\n--origin <RepoLink>: Sets the current repo origin to the link given"
                                    "\n--setbranch <BranchName>: Sets the branch to push the data later on (example: \"main\" or \"old\")"
                                    "\n--trackadd <filename>/<directory>/<.>: filename is added, directory means full directory is added, <.> is for current directory adding."
                                    "\n--getdata <depth: ExampleIntNumber>: Pulls the data from the repo"
                                    "\n--pushdata: Pushes the data locally to the repo.")
                        if "--version" in sys.argv[1]:
