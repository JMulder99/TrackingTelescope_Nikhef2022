# Tracking Telescope Nikhef Project 2022
The repository for the code from the 2022 Tracking Telescope Nikhef project. The collaborators can be find below. The description of each team is explained in their own README within the subfolder. Below that, you will find instructions to **clone** this repository to your desktop and make a first **commit** and **push request** to this README. Further tips follow below.  

## Teams
The collaboration consists of the following teams:

### Lead developer 


### Detector and hardware construction and testing


### Data acquisition and quality control


### Simulation and Track reconstruction


## First commit
Open the **command prompt** and use 
```
cd ~ # to go home
mkdir <foldername> # name of you git repository/folder
cd <foldername>
```
to create a new folder. Then, you are ready to **clone** this repository to your device. Use the following if you clone over HTTPS:
```
git clone https://github.com/JMulder99/TrackingTelescope_Nikhef2022
```
or the following if you clone of SSH:
```
git clone git@github.com:JMulder99/TrackingTelescope_Nikhef2022.git
```
Note that any git command is lead by `git`.

Now use `ls -a` or a similar command to print all files (names) that you just cloned. Now you are ready for your first **commit**. Open this README file using your favorite text-editor. You can search online how to do this (and how to save and close the editor!). Then 
```
git add README.md #add the file you just edited to be staged

git status # can be used to see the status of your commit

git commit -m "<Short description of your edit>" #commit the file
```
Now you have just "updated" your local **main branch** with your latest changes. To update the **remote** repository, you should **push** the commit to GitHub and ask for your change to be **merged** into the github main branch.
```
git push remote main  # git push <remote repository alias> <local branch>
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