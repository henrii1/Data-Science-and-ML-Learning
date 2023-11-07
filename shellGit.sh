#use git bash to run these unix commands

# creating a new file on command line
touch filename.filetype
# creating folders
mkdir folder name
# opening vscode 
code filename.filetype
# showing the manual for each command
man command_name
# lists
ls -l # list files and shows read or write permissions
ls -a # list all files and directories, including hidden ones
la -la # does both r=read, rw=write, x=executable code
pwd # print working directory
cp or copy # copies files to another directory
mv or move # moves files

vim testshell.sh
# press i key for insert mode
#!/bin/bash    this signifies it is a bash file
echo 'hello world'
# press escape to get out of insert mode
type ':wq!' to save the file
chmod 755 testshell.sh # chmod 755 adds the x permision to the file, making it executable
./testshell.sh # this runs the file.

ls # list directories 
cd .. # lets us move backward the directory
cd full_path # moves back to wherever

mkdir directory_name

mv submissions archive # moving submissions file or folder to archive directory


cat filename.filetype # prints the content of the file
# after opening the file, run the command below
wc filename.filetype -w # -w specifies the word count as output
# Pipes (allow to pass output of one command as input into another)

ls | wc -w # returns the number of files in the current directory.
cat file_name.type | wc -w # word count

cat file1.type file2.type | wc -w # returns the total word count for the two files

# Redirections (with redirections, we can change the standard input (keyboard) and output (screen) to others)

 # '< output', ''> input' everything typed on command line is saved as a file, use pipes to control where to save
cat > input.txt # > specifies there the input goes to
# add text into the input.txt file
# press ctrl + D to signify the end of the file
cat < input.txt # < specifies output

ls -l > output.txt #  > specifies where we want the output of ls -l to go (into the output.txt file)
less output.txt # helps u view the content of output.txt

# errors usually occure, it is common practice to write errors to another file
ls -l /bin/usr > error.txt # path is invalid so machine prints that on cmd
ls -l /bin/usr 2> error.txt # now the error is printed into the error.txt file
less error.txt # display output

ls -l /bin/usr > error_output.txt 2>&1 # saves list or error into file
less error_output.txt

# Grep (global regular expression print) searching across file, folders and the content of files
Grep sam names.txt # returns all words with sam in their spelling in names.txt

grep -i sam names.txt # Grep is case sensitive, this is how to make it not

grep -w sam names.txt # returns only a full match, no partial matches (eg 'sam' and not'sama')

ls /bin |grep -i zip # using the pipe with grep to find zip files
clear # clears screen

# Git and Github
#NB. any folder starting with a '.' is a hidden folder
git init # adds the .git file that tracks all changes

git restore --stage filename.type # returns an added file back to untracked area.

git checkout -B newbranch name # creates a new branch and moves into
git branch newbranch name # creates a branch too
git checkout newbranch name # moves into

git push -u origin newbranch name # pushes only to that branch

#NB: after merging a pull request, it is important to checkout to main and run a git pull

mkdir myrepo | cd myrepo
git init
git remote add origin shh or url link
git remote -v # displays the remote
git pull
git checkout main # creates a local main
ls # display the remote contents of main

cd .git
cat HEAD # displays the tracked branch name we are currently on
cat /refs/heads/main # displays the has id for the current commit. changes after every commit, can be tracked by git log
# NB: this link is displayed as output from cat HEAD


# GIT Diffs (revisit changes)
git diff HEAD filechanged.type # compares the head commit with the file.
git log --pretty = oneline # makes log more readable
git diff hashID_commit1 hashID_commit2 # shows the difference between two commit id

git main newbranch # will display changes btwn the two branch


# git BLAME  (returns all the changes made to a file)

git blame filename.type # returns all changes, when, how, hash and change on the file
# change order: Developer_hash(unique for each dev), dev_name, datetime, line_no, change_implemented

git blame -L 5,15 filename.type # returns changes for codeline 5 to 15
git log -p hashId # returns the actual change with this ID

