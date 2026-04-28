# RepoM Docs
*This branch of RepoM repository is dedicated to only documentation regarded to _RepoM_, any issues may be reported in the main branches issues.*

# Hello!

##### Hi, welcome to RepoM documentation. We will be calling this RepoMd from now on!
----------------------------------------------------------------------------------------------------------------------
<details>
<summary>Chapter? 1, Repository Basics</summary>

### Making a repository

*RepoM* allows you to make repos without interfering with the browser.

Although you'll need to make a token, to make a token, check out the github docs.
[Link TO Github Docs for Token Making](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

Now, once you have a token ready, do these steps:

+ Do ```repos --cleartoken``` & ```repos --makerepo WhateverNameYouWantToPut```.
+ At the --makerepo command, prepare your *classic token* (Maybe copy it?)
+ When it asks for your token, try pasting it or typing it (Note: if ctrl+v doesnt work, try right-clicking to paste it...)
+ Check if the repo was made.

+ Bonus: To set the repo made as the origin, do this: ```repos --makerepo RepoName --set_asorigin```

---------------------------------------------------------------------------------------------------------------------------------------------

### Deleting a repository
To delete a repository, follow this lone step:
+ Do ```repos --delete YourUserName YourRepoName```.

*YourRepoName* is the repository name, *YourUserName* is the username the repository was created inside... 

------------------------------------------------------------------------------------------------------------------------------------------------

</details>

<details>
<summary>Chapter? 2, Commit then push</summary>

*Next up*:
+ Adding files
+ Commiting Files
+ Pushing Files
+ Pulling Files

### Adding files

We need to understand what 'add a file' means, for newbies, it might mean adding a file to another file (Not really?)...

*Add a file* means that *git* will track it and it will be considered in any 'commit' that is made.

---------------------------------------------------------------------------------------------------------------------------------------------------
To add a file, follow these step(s):
+ ```repos --addfile <File>/<Dir>/<.>```
-----
Now, --addfile calls ```git add <File>``` behind the scenes.

The *arguments* are intresting here!

File corrspond to any file that you put as a argument.

Dir represents to any directory that you put as a argument.

. represents the 'Current directory' or the directory you are cded into.

-------------------------------------------------------------------------------------------------------------------------------------------------------

### Commiting files

To *commit* a file, follow these step(s):
+ ```repos --commit "Test message"```
This command will commit the files added with the message in the string.

------------------

### Pushing files

To push a file, follow these step(s):
+ ```repos --pushfile <BranchName>```

This pushes the commited files to the branch given as the branchname argument.

-------

### Pulling files

To pull a file, follow these step(s):
+ ```repos --pullfile <BranchName>```

This pulls the latest commit files from the branch given as the branchname argument.


------

</details>

## If your seeing this too early!

*Just know only the BASICS are completed for now*

*THIS IS NOT FULLY FINISHED*