# Git and GitHub Commands Guide

## 1. Initial Setup (初期設定)

- **Set global username:**
  `git config --global user.name "Your Name"`
- **Set global email:**
  `git config --global user.email "your.email@example.com"`
- **Check configuration:**
  `git config --list`

## 2. Creating and Cloning Repositories (リポジトリの作成とクローン)

- **Initialize a new Git repository:**
  `git init`
- **Clone an existing repository:**
  `git clone <repository-url>`

## 3. Basic Workflow (基本的なワークフロー)

- **Check status:**
  `git status`
- **Add a file to the staging area:**
  `git add <file-name>`
- **Add all modified/new files to staging:**
  `git add .`
- **Commit changes with a message:**
  `git commit -m "Commit message"`
- **Amend the last commit:**
  `git commit --amend`

## 4. Viewing History (履歴の確認)

- **View commit history:**
  `git log`
- **View a condensed commit history:**
  `git log --oneline`
- **View changes made to files:**
  `git diff`

## 5. Branching and Merging (ブランチとマージ)

- **List all local branches:**
  `git branch`
- **List all branches (local and remote):**
  `git branch -a`
- **Create a new branch:**
  `git branch <branch-name>`
- **Switch to a branch:**
  `git checkout <branch-name>`  *(or `git switch <branch-name>`)*
- **Create and switch to a new branch:**
  `git checkout -b <branch-name>` *(or `git switch -c <branch-name>`)*
- **Merge a branch into the current branch:**
  `git merge <branch-name>`
- **Delete a local branch:**
  `git branch -d <branch-name>`

## 6. Remote Repositories (リモートリポジトリ)

- **List remote repositories:**
  `git remote -v`
- **Add a new remote repository:**
  `git remote add origin <repository-url>`
- **Push changes to remote repository:**
  `git push origin <branch-name>`
- **Fetch changes from remote repository:**
  `git fetch`
- **Pull changes from remote repository (fetch + merge):**
  `git pull origin <branch-name>`

## 7. Stashing (スタッシュ)

- **Stash current changes:**
  `git stash`
- **List all stashes:**
  `git stash list`
- **Apply the latest stash:**
  `git stash apply`
- **Apply and remove the latest stash:**
  `git stash pop`

## 8. Undoing Changes (変更の取り消し)

- **Unstage a file:**
  `git restore --staged <file-name>`
- **Discard changes in working directory:**
  `git restore <file-name>`
- **Revert a commit (creates a new commit reverting changes):**
  `git revert <commit-hash>`
- **Reset commit history (moves HEAD):**
  - **Soft reset (keep changes in staging):** `git reset --soft <commit-hash>`
  - **Mixed reset (keep changes in working directory):** `git reset HEAD~1` (default)
  - **Hard reset (discard all changes):** `git reset --hard <commit-hash>`

---

## GitHub CLI (`gh`) Commands

If you have the [GitHub CLI](https://cli.github.com/) installed, you can use these commands to interact with GitHub directly from your terminal.

- **Authenticate with GitHub:**
  `gh auth login`
- **Clone a repository:**
  `gh repo clone <owner>/<repo>`
- **Create a new repository on GitHub:**
  `gh repo create <repo-name> --public` *(or `--private`)*
- **Create a Pull Request:**
  `gh pr create --title "PR Title" --body "PR Description"`
- **List open Pull Requests:**
  `gh pr list`
- **Checkout a Pull Request locally:**
  `gh pr checkout <pr-number>`
- **View an issue:**
  `gh issue view <issue-number>`
- **Create a new issue:**
  `gh issue create --title "Issue Title" --body "Issue details"`
