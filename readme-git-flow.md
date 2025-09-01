Git Workflow Commands
This guide provides a complete, step-by-step Git workflow from initializing a new repository to pushing your changes to a remote server. The commands assume you have already cd'd into your project directory named esmaulhusna.


## MacOS: Add steps to authenticate github using PAT classic


## Windows: Add steps to authenticate github using PAT classic

## For both: Add steps to authenticate github using PAT fine tuned access

## Step 1: Set Your User Information
This is a one-time setup on your machine to identify your commits. Use the email associated with your Git account.

Run:
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 2: Initialize a Local Git Repository
This command creates a new, empty Git repository in the current directory.
Run:
```
git init
```

## Step 3: Add Your Files
This command stages all the files in your project for the first commit. The . refers to all files in the current directory.
Run:
```
git add .
```

## Step 4: Make Your First Commit
This command saves the staged changes to your local repository. The message should be a short, descriptive summary of the changes.

Run:
```
git commit -m "Initial commit of the Esma-ül Hüsna CLI project"
```

## Step 5: Connect to a Remote Repository
You need to create a new, empty repository on a hosting service like GitHub, GitLab, or Bitbucket. Then, copy the remote repository URL and use it in this command.

Run:
```
git remote add origin [https://github.com/your-username/esmaulhusna.git](https://github.com/your-username/esmaulhusna.git)
```
## Step 6: Push Your Files to the Remote Repository
This command pushes your local commits to the main branch of your remote repository. The -u flag sets the upstream, so future pushes can be done with just git push.

Run:
```
git push -u origin main
```
