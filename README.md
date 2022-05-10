# Tracking Telescope Nikhef Project 2022
The repository for the code from the 2022 Tracking Telescope Nikhef project. The collaborators can be find below. The description of each team is explained in their own README within the subfolder. Below that, you will find instructions to **clone** this repository to your desktop and make a first **commit** and **push request** to this README. Further tips follow below.  

## Teams
The collaboration consists of the following teams:

### Lead developer 
Jelmer Mulder #added this line from nikhef account

### Detector and hardware construction and testing
Isis Hobus  #added this line from nikhef account
<br />Evi Nikoloudaki 
<br />Guoxi Zhu #added this line from nikhef account
<br />Dylano van Oijen #added this line from nikhef account
<br />Viktoriia Tulaidan #added this line from nikhef account 
<br />Svitlana Hoienko #added this line from nikhef account
<br />Aliwen Delgado #added this line from nikhef account

### Data acquisition and quality control
Jelmer Mulder #added this line from nikhef account
<br />Steven Niedenzu #added this line from nikhef account


### Simulation and Track reconstruction
Evi Nikoloudaki
<br />Maurice Geijsen
<br />Jasper Westbroek #added this line from nikhef account
<br />Dylano van Oijen #added this line from nikhef account
<br />Aliwen Delgado #added this line from nikhef account

## Update
If you copied the 'dot' files in during the Canvas quiz, the .ssh/config file has be changed. You need to redo the ssh-over-https by adding the following lines:
```
Host github.com
Hostname ssh.github.com
Port 443
User git
```
You should also comment out the following line in the .ssh/config file: change `IdentityFile ~/.ssh/nikhef_rsa` to `#IdentityFile ~/.ssh/nikhef_rsa` to use your public ssh keys that you coupled to your github account. 


## Linking nikhef computer account to Github account over SSH
To simplify the login process on the command line, a SSH connection can be set up with your GitHub account. This is a scary and bit complex process, but I am going to refer to [the Github website](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh) where it is nicely explained. Check left navigation bar for the different steps. Generially, you need to
1) [Add Github email to git](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-email-preferences/setting-your-commit-email-address) on nikhef account
2) check for existing SSH keys (our nikhef accounts are fresh, so this can be skipped)
3) Create the SSH keys on nikhef computer (passphrase can be skipped by pressing enter when asked)
4) Copy the public key and add it to personal Github account
5) Test connection

Testing the connection may fail, you might see `Timeout: port 22 is not available`. Please take a look at (SSH cloning over HTTPS connection)[https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port]. Then, clone using the SSH link below.

**Tip!** To copy text in and out of the les-center environment, you need to use the blue hovering arrow on the edge of the screen. You can past text in the clipboard section, then hover over text (selecting it with your cursor) to have it copied to the les-center environment. Note that anything that is selected in  les-center is automatically copied to your clipboard. Use right-press to paste in the command line. It may be easier to open the Github website on the internet browser inside les-center. 

## Being added as collaborator
I will add everyone with a Github account as a collaborator to our Github repository. 

## First commit
Open the **command prompt** and use 
```
cd ~ # to go home

EDIT:
mkdir <foldername> # name of you git repository/folder
cd <foldername>
# Instead of doing these lines above, you can directly clone the repository. 
# It creates its own folder. Doing the above creates the cloned repository inside your subfolder. 
```
to create a new folder. Then, you are ready to **clone** this repository to your device. Use the SSH method ((even if SSH not working directly and you used the config option))[https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port]
```
git clone git@github.com:JMulder99/TrackingTelescope_Nikhef2022.git
```
Otherwise, you can clone over HTTPS:
```
git clone https://github.com/JMulder99/TrackingTelescope_Nikhef2022
```

Note that any git command is lead by `git`.

Now use `ls -a` or a similar command to print all files (names) that you just cloned. Now you are ready for your first **commit**. Open this README file using your favorite text-editor. You can search online how to do this (and how to save and close the editor!). Then 
```
git add README.md #add the file you just edited to be staged

git status # can be used to see the status of your commit

git commit -m "<Short description of your edit>" #commit the file
```
Now you have just "updated" your local **main branch** with your latest changes. To update the **remote** repository (Use `git remote` to print out the name of the remote), you should **push** the commit to GitHub and ask for your change to be **merged** into the github main branch.
```
git push origin main  # git push <remote repository alias> <local branch>
```
After that, anyone can use `git pull` to update their local repository with your update (and any changes done by others at that time). 

# Good practices
## Usefull git commands
Checkout [this git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf) for most important git commands. You can also call 
```
git help
```
to print out an usefull list of most commands. You are encouraged to search any additional problem online. 

## Usefull command line commands
Checkout [this linux command line cheat sheet](https://cheatography.com/davechild/cheat-sheets/linux-command-line/). The "Directory Operations" with "ls options" are usefull to navigate in the command-line; "File Operations" are usefull to create, open etc files and "Nano Shortcuts" (the standard text editor) is usefull to edit `.txt` files and alike. 

## Plots
You should save plots as pdf's as they are vector images (zoom-able), but not upload them to git(hub). 

## Branches
If you are creating any new function/edition that might break your code, it is best to create a new **branch**.
```
git branch <new branch> #usually the name of the new functionality
```
You can view a git repository as a growing tree. The **main branch** is the central trunk, and new branches may grow beyond the main trunk. If the code is finished and works (!!!), you should "reposition yourself" to the main branch by
```
git checkout main
```
and then **merge** your edited branch with the main branch.
```
git merge <new branch> # into the main
```
Note, this can raise a **merge conflict** which should be resolved immediately. See below. 

## .gitignore
Git(Hub) is a version control system which means every edition of all files that are being tracked are saved. Of course, this is a great advantages when working on code, but it also can be messy when wrong files are uploaded. This is solved by `.gitignore`. All specific files (e.g. `data.txt`), file extensions (e.g. `.pdf`) or folders (e.g. `/Images/`) named in `.gitignore` are never committed or uploaded to github. The current `.gitgnore` already holds many general file extensions, but you may add file (extensions)/folders yourself and use the `git add/commit` and `git push` processes to update it for everybody. Generally, you do not want to upload images (they can be reproduced by your code), data files (these are saved only locally), pdf-files, or any other files not imported to keep all versions off. 

# Troubleshooting
If these instructions nor internet has resolved your issue, please contact Jelmer Mulder (@JMulder99).

## Merge conflicts
Unlike Google Drive, editors work locally which means any updates are not synced immediately to others. In most cases, git automatically merges your changes with others, but it may happen that you've deleted a line which was edited by someone else. Git does not know how to merge these changes and raises a **merged conflict**. It automatically opens an in-line file editor with the two conflicting files next to eachother. The conflicting lines are highlighted. You should (by-hand) resolve the conflicts by deciding which lines to keep/delete. You save the changes, add and commit them. The conflict should be resolved. This proces is explained more clearly in [the following webpage](https://opensource.com/article/20/4/git-merge-conflict) from 'Merge the branch into master to see the error:' onwards. 
