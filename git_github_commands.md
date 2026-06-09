# GitとGitHubのコマンドガイド

## 1. 初期設定 (Initial Setup)

- **グローバルなユーザー名を設定する:**
  `git config --global user.name "Your Name"`
- **グローバルなメールアドレスを設定する:**
  `git config --global user.email "your.email@example.com"`
- **設定を確認する:**
  `git config --list`

## 2. リポジトリの作成とクローン (Creating and Cloning Repositories)

- **新しいGitリポジトリを初期化する:**
  `git init`
- **既存のリポジトリをクローンする:**
  `git clone <repository-url>`

## 3. 基本的なワークフロー (Basic Workflow)

- **状態を確認する:**
  `git status`
- **ファイルをステージングエリアに追加する:**
  `git add <file-name>`
- **変更・新規作成されたすべてのファイルをステージングに追加する:**
  `git add .`
- **メッセージを付けて変更をコミットする:**
  `git commit -m "Commit message"`
- **直前のコミットを修正する:**
  `git commit --amend`

## 4. 履歴の確認 (Viewing History)

- **コミット履歴を表示する:**
  `git log`
- **コミット履歴を1行で簡潔に表示する:**
  `git log --oneline`
- **ファイルに加えられた変更を表示する:**
  `git diff`

## 5. ブランチとマージ (Branching and Merging)

- **ローカルのすべてのブランチを一覧表示する:**
  `git branch`
- **すべてのブランチ（ローカルとリモート）を一覧表示する:**
  `git branch -a`
- **新しいブランチを作成する:**
  `git branch <branch-name>`
- **ブランチを切り替える:**
  `git checkout <branch-name>`  *(または `git switch <branch-name>`)*
- **新しいブランチを作成して切り替える:**
  `git checkout -b <branch-name>` *(または `git switch -c <branch-name>`)*
- **現在のブランチに別のブランチをマージする:**
  `git merge <branch-name>`
- **ローカルブランチを削除する:**
  `git branch -d <branch-name>`

## 6. リモートリポジトリ (Remote Repositories)

- **リモートリポジトリを一覧表示する:**
  `git remote -v`
- **新しいリモートリポジトリを追加する:**
  `git remote add origin <repository-url>`
- **リモートリポジトリに変更をプッシュする:**
  `git push origin <branch-name>`
- **リモートリポジトリから変更をフェッチ（取得）する:**
  `git fetch`
- **リモートリポジトリから変更をプル（取得してマージ）する:**
  `git pull origin <branch-name>`

## 7. スタッシュ (Stashing)

- **現在の変更を一時的に退避（スタッシュ）する:**
  `git stash`
- **すべてのスタッシュを一覧表示する:**
  `git stash list`
- **最新のスタッシュを適用する:**
  `git stash apply`
- **最新のスタッシュを適用して削除する:**
  `git stash pop`

## 8. 変更の取り消し (Undoing Changes)

- **ファイルのステージングを取り消す:**
  `git restore --staged <file-name>`
- **作業ディレクトリの変更を破棄する:**
  `git restore <file-name>`
- **コミットを取り消す（変更を取り消す新しいコミットを作成）:**
  `git revert <commit-hash>`
- **コミット履歴をリセットする（HEADを移動）:**
  - **Softリセット（変更をステージングに残す）:** `git reset --soft <commit-hash>`
  - **Mixedリセット（変更を作業ディレクトリに残す）:** `git reset HEAD~1` (デフォルト)
  - **Hardリセット（すべての変更を破棄）:** `git reset --hard <commit-hash>`

---

## GitHub CLI (`gh`) コマンド

[GitHub CLI](https://cli.github.com/)がインストールされている場合、これらのコマンドを使用してターミナルから直接GitHubを操作できます。

- **GitHubで認証する:**
  `gh auth login`
- **リポジトリをクローンする:**
  `gh repo clone <owner>/<repo>`
- **GitHubに新しいリポジトリを作成する:**
  `gh repo create <repo-name> --public` *(または `--private`)*
- **プルリクエストを作成する:**
  `gh pr create --title "PRのタイトル" --body "PRの説明"`
- **開いているプルリクエストを一覧表示する:**
  `gh pr list`
- **プルリクエストをローカルにチェックアウトする:**
  `gh pr checkout <pr-number>`
- **Issueを表示する:**
  `gh issue view <issue-number>`
- **新しいIssueを作成する:**
  `gh issue create --title "Issueのタイトル" --body "Issueの詳細"`