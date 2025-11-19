import streamlit as st
from pathlib import Path
import yaml
import os




def manage_repo_list():
    
    # Pad naar de directory van dit script
    base_dir = Path(__file__).parent

    # Relatief pad naar de YAML-file
    repo_file = base_dir.parent / "app" / "config" / "repos.yaml"

    # Load repositories from YAML
    def load_repositories():
        if os.path.exists(repo_file):
            with open(repo_file, "r") as f:
                return yaml.safe_load(f) or []

    # Save repositories to YAML
    def save_repositories(repositories):
        with open(repo_file, "w") as f:
            yaml.safe_dump(repositories, f)

    # Initialize repositories in session state
    if "repositories" not in st.session_state:
        st.session_state.repositories = load_repositories()

    st.markdown('<h3 style="margin-bottom:0;">📂 Available repositories:</h3>', unsafe_allow_html=True)


    # Display current repositories with delete buttons
    for i, repo in enumerate(st.session_state.repositories):
        col1, col2 = st.columns([0.9, 0.1])
        col1.write(repo)
        if col2.button("❌", key=f"delete_{i}"):
            st.session_state.repositories.pop(i)
            save_repositories(st.session_state.repositories)
            st.rerun() 
    
    st.divider()

    # Input field for a new repository
    new_repository = st.text_input("URL", placeholder="Add GitHub SSH url")

    col1, col2  = st.columns([2,8], gap="small", vertical_alignment="top")

    with col1:
      if st.button("➕ Add") and new_repository:
          st.session_state.repositories.append(new_repository)
          save_repositories(st.session_state.repositories)
          st.success(f"Repository '{new_repository}' added!")

          st.rerun() 

    with col2:
      # Optional: reset to default repositories
      if st.button("🔄 Clear All"):
          default_repositories = [
              
          ]
          st.session_state.repositories = default_repositories
          save_repositories(default_repositories)
          st.info("Repositories are removed")
          st.rerun() 
