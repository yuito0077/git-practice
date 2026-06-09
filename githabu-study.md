# Git / GitHub 基礎学習ノート (2026-06-09)

## 1. GitとGitHubの全体像
- **Git（ローカル）**: 自分のMacの中でファイルの変更履歴を記録する「道具」。
- **GitHub（リモート）**: その履歴をネット上で保存・共有する「場所」。

---

## 2. 初期設定・確認コマンド
Gitに「誰が履歴を刻んでいるか」を教えるためのコマンド。

```bash
# Gitのバージョンを確認する
git --version

# ユーザー名とメールアドレスを登録する（メールはGitHubと同じものにする）
git config --global user.name "yuito"
git config --global user.email "dev@yuito0077.com"

# 登録されている設定を一覧表示する
git config --global --list

# 【復習ポイント】間違えて登録したタイポ（user.emaillなど）を削除する
git config --global --unset user.emaill

# 現在のフォルダをGitの管理下（リポジトリ）にする（最初の1回だけ）
git init

# 【最重要】今どのファイルがどのエリアにあるか、状態を泥臭く確認する
git status

# ワークツリーの変更をステージングエリア（荷出し場）に載せる
git add readme.md
# ※フォルダ内のすべての変更をまとめて載せる場合は「git add .」

# ステージングエリアの荷物を、メッセージ付きで倉庫に永久保存する
git commit -m "it commit test."

# これまで倉庫に積み重ねてきたコミットの歴史を一覧する
git log

# ブランチの一覧と、自分が今いる現在地（* がつく）を確認する
git branch

# 「test」という名前の新しい枝（ブランチ）を作成する（作っただけでは移動しない）
git branch test

# 「test」ブランチに自分の現在地を切り替える
git checkout test
