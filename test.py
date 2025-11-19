from git import Repo, GitCommandError, RemoteProgress
import os
import shutil
import tempfile
import subprocess


def get_remote_branches(repo_url: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--heads", repo_url],
            check=True,
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().split("\n")
        branches = [line.split("refs/heads/")[1] for line in lines if "refs/heads/" in line]
        return sorted(set(branches))
    except subprocess.CalledProcessError as e:
        st.error(f"Fout bij ophalen van branches: {e.stderr}")
        return []

CLONE_DIR = "cloned_repos"
os.makedirs(CLONE_DIR, exist_ok=True)

repo_url = 'git@github.com:vanadengage/dbt-workforce-management.git'
custom_dir = 'test'
repo_name = custom_dir.strip() or os.path.splitext(os.path.basename(repo_url))[0]
target_path = os.path.join(CLONE_DIR, repo_name)
selected_branch = 'sandbox/dbt_ahu__agg_aad'
Repo.clone_from(repo_url, target_path, branch=selected_branch)