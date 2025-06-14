import requests
import streamlit as st

ORG_NAME = 'alphatechlogics'
GITHUB_API_URL = f'https://api.github.com/orgs/{ORG_NAME}/repos'



for i, repo in enumerate(all_repos):
    if not isinstance(repo, dict):
        st.write(f"Item {i} is not a dict! It's {type(repo)}: {repo}")
    else:
        # Also check if 'name' key exists
        if 'name' not in repo:
            st.write(f"Item {i} has no 'name' key: {repo}")

response = requests.get(GITHUB_API_URL)
st.write("Status code:", response.status_code)
st.write("Response JSON:", response.json())
