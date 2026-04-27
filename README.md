# RepoManagement
*RepoManagement* is a program made in Python 3.13, its purpose is to wrap Git & Allow more features to be used.

After downloading it and running it, you have to do only 1 thing...
Make a PAT (Personal Access Token)/Classic Token in github (Read the ```# Token Making``` section for instructions)

and you'll never have to touch github.com again (hopefully?)

----------------------------------------------------------------------------------------------------------------------

# Installing & Setting up
To install the program *(we'll call it RepoM now!)*, follow these steps:

## Installing

+ Go to the github releases and get any latest release.
+ Place the executable somewhere
+ Add the location where you placed the executable to your PATH (Read in ```# How to add in PATH```)
+ Check using ```repos --version```, & yes. Its called repos in the executable name, i dont know why but its called that. (i didnt notice while making it)
## Setting up
+ Do ```repos --cleartoken``` & ```repos --makerepo WhateverNameYouWantToPut```.
+ At the --makerepo command, prepare your *classic token* (Maybe copy it?)
+ When it asks for your token, try pasting it or typing it (Note: if ctrl+v doesnt work, try right-clicking to paste it...)
+ Check if the repo was made.
+ If you want to delete the repo you made, do ```repos --delete YourUser YourRepoName```.

_All done! Your *RepoM* setup has been completed for later uses_

----------------------------------------------------------------------------------------------------------------------

# Token Making (Important!)
To make a Classic token or a PAT, follow these steps:

+ Go to [Token Making/Handling Page] (https://github.com/settings/tokens) or https://github.com/settings/tokens.
+ Click on ```Personal Access Tokens```, and click on ```Tokens (Classic)```
+ Click on the ```Generate New Token``` button, and click on ```Generate New Token (Classic)```
+ Now, do whatever security checkup github gives you (Like a passkey)
+ You will be asked for names and a ton of options.
+ Enter any name you want (Example: *MyTokenForRepoM*)
+ Change the date to your likings (NOTE: The date of expiration is when the token will not work anymore, and you will have to make a new token and clear the old token using ```repos --cleartoken```)
+ Now on the select scopes options, Select the repo option, workflows option, write:packages option and delete:packages option, the user option, delete_repo option and admin:public_key.
+ Click on ```Generate token```.
+ Copy the token and paste it somewhere safe and somewhere you'll not forget, now follow the ```# Installing & Setting up``` sections 'Setting up' instructions)

----------------------------------------------------------------------------------------------------------------------

# How to add in PATH
To add *RepoM* to your PATH, follow these steps:
+ Copy the location where the executable lives.
## For Windows:

+ Search *View Advanced System Settings* & open it.
+ Click on Environmental Variables
+ Click on the PATH button below *<u>U</u>ser Variables*
+ Click on new & paste the path & press enter.
+ Click on _OK_ on every box.

## For linux:

+ Do *echo $0* or *echo $SHELL*
+ If it returns, Bash or Zsh, Do the below:

### For Bash:
+ Open ~/.zshrc in any text editor
+ Scroll to the bottom of the file, and do ```export PATH="$PATH:/your/new/path"```, but the /your/new/path is a placeholder to the path where the executable lives.
+ Do ```source ~./bashrc```
### For Zsh:
+ Open ~/.zshrc in any text editor
+ Scroll to the bottom of the file, and do ```export PATH="$PATH:/your/new/path"```, but the /your/new/path is a placeholder to the path where the executable lives.
+ Do ```source ~./zshrc```

---------------------------------------------------------------------------------------------------------------------

# Bug reports

To sumbit a bug report, make a new issue with any labels you want & describe it in detail if possible for maximum clarity...

------------------------------------------------------------------------------------------------------------------------
# Contributing
*Contributing* is helpful, fork the repo, and put your name in the file *contribute.adf* in this format:

```YourName - DateOfContribution``` or ```YourGithubUsername - DateOfContribution```

-----------------------------------------------------------------------------------------------------------------------

# LICENSE

*GPL 3*, located in source code inside the REPO.




