import streamlit as st
from forms.settings import manage_repo_list
from app.functions import load_repositories
from git import Repo, GitCommandError, RemoteProgress
from pathlib import Path
import os
import shutil
import tempfile
import subprocess
import tempfile
import yaml

### Settings
# clone_dir = "/mnt/host_dbt"
clone_dir = "/root/dbt/"
os.makedirs(clone_dir, exist_ok=True)

base_dir = Path(__file__).parent
repo_file = base_dir.parent / "app" / "config" / "repos.yaml"

# Load repositories from YAML
repos = load_repositories(repo_file)


### Functions
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
        st.error(f"Error in collecting branches: {e.stderr}")
        return []

@st.dialog("Manage repository List")
def show_manage_repo():
    st.markdown('Here you can add and remove the repository list\n\n')
    manage_repo_list()


### Page

st.title("🔁 Data Engineering Toolkit")
st.subheader("")


if st.button("⚙️ manage repositories"):
    show_manage_repo()

st.divider()    

with st.container():
    col1, col2  = st.columns([4, 6], gap="small", vertical_alignment="top")

    with col1:
        repo_url = st.selectbox("📂 Choose Repository", repos)

    with col2:
        st.markdown("\n\n\n\n")
        # Session state to store available branches
        if "branches" not in st.session_state:
            st.session_state.branches = []

        if st.button("🔍 Get branches"):
            if not repo_url:
                st.warning("Add valid Git repo-URL.")
            else:
                branches = get_remote_branches(repo_url)
                if branches:
                    st.session_state.branches = branches
                    st.success(f"Branches found")
                else:
                    st.error("No branches found")

col1, col2  = st.columns([4, 6], gap="large", vertical_alignment="top")


with col1:
    

    # Step 3: Select branch (if available)
    if st.session_state.branches:
        selected_branch = st.selectbox("📂 Select branch", st.session_state.branches)
    else:
        selected_branch = None

    st.markdown('Clone Repo')
    # Optional: repo naam kiezen (i.p.v. automatisch)

    is_pr = st.checkbox("🚨 Is review")

    if is_pr:
        custom_dir = st.text_input("🗂️ Enter PR#", placeholder="Enter PR#")
    else:
        custom_dir = st.text_input("🗂️ Name of local folder (optional)", "")

    overwrite = st.checkbox("🚨 Overwrite if folder already exists")

    if st.button("📥 Clone repo"):
        if not repo_url or not selected_branch:
            st.warning("Insert repo URL and choose branch.")
        else:
            repo_name =  os.path.splitext(os.path.basename(repo_url))[0]

            if custom_dir:
                repo_folder = custom_dir.strip()
            else:
                repo_folder = selected_branch.strip()

            target_path = os.path.join(clone_dir, repo_folder, repo_name)

            # Check if directory exists
            if os.path.exists(target_path):
                if overwrite:
                    try:
                        shutil.rmtree(target_path)
                        st.info(f"Existing folder '{repo_name}' has been deleted.")
                    except Exception as e:
                        st.error(f"Unable to remove existing folder: {e}")
                        st.stop()
                else:
                    st.error(f"Folder '{repo_name}' already exists. Chech 'over write' to proceed.")
                    st.stop()

            try:
                Repo.clone_from(repo_url, target_path, branch=selected_branch)
                st.success(f"Repo successfully cloned to:\n{target_path}")
            except GitCommandError as e:
                st.error(f"Error during cloning: {e}")

with col2:
    st.subheader("🔁 New Git-Branch")
       

    new_branch_name = st.text_input("Voer de naam van de nieuwe branch in:")

    if st.button("Maak branch aan"):
        if not repo_url.strip():
            st.error("⚠️ Vul een geldige repo URL in.")
        elif not new_branch_name.strip():
            st.error("⚠️ Vul een geldige branchnaam in.")
        else:
            # Tijdelijke folder om de repo te clonen
            with tempfile.TemporaryDirectory() as tmpdirname:
                try:
                    st.info("🔄 Repo clonen...")
                    repo = Repo.clone_from(repo_url, tmpdirname)

                    # Check of main bestaat
                    main_branch_name = "main" if "main" in repo.heads else "master"
                    main_branch = repo.heads[main_branch_name]

                    # Nieuwe branch aanmaken vanaf main
                    if new_branch_name in repo.heads:
                        repo.heads[new_branch_name].checkout()
                        st.warning(f"Branch '{new_branch_name}' bestaat al, er naartoe geswitched!")
                    else:
                        new_branch = repo.create_head(new_branch_name, commit=main_branch.commit)
                        new_branch.checkout()
                        st.success(
                            f"✅ Branch '{new_branch_name}' succesvol aangemaakt vanaf {main_branch_name}!\n\n"
                            "🔄 Pushen naar remote..."
                        )
                        # Push nieuwe branch
                        origin = repo.remote(name="origin")
                        origin.push(new_branch_name)
                        st.success(f"✅ Branch '{new_branch_name}' succesvol gepusht naar remote!")

                except GitCommandError as e:
                    st.error(f"Fout bij Git-operatie: {e}")
                except Exception as e:
                    st.error(f"Er is iets misgegaan: {e}")