import streamlit as st
import pathlib

st.set_page_config(layout="wide")

# Function to load CSS from the 'assets' folder
# def load_css(file_path):
#     with open(file_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# # Load the external CSS
# css_path = pathlib.Path("assets/styles.css")
# load_css(css_path)





# --- page set up ---

about_page = st.Page(
  page = "pages/about_me.py",
  title = "About Me",
  icon = ":material/account_circle:",
  default= True,
)
project = st.Page(
  page = "pages/projects.py",
  title = "My Projects",
  icon = ":material/smart_toy:",
)

git = st.Page(
  page = "pages/git.py",
  title = "Git Repo Manager",
  icon = ":material/smart_toy:",
)

settings= st.Page(
  page = "pages/toolkit.py",
  title = "Toolkit",
  icon = ":material/smart_toy:",
)



pages = [git, about_page, project,  settings]





# --- on all pages ---

# st.logo ()
st.sidebar.text("Made by Chris Boonstra")




# --- navigation setup ---
pg = st.navigation(pages, position="top")

# --- run navigation ---
pg.run()