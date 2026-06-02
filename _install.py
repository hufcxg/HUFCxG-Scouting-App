#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess, sys

def ensure_installed():
    try:
        import hufcxg_scout
    except ImportError:
        import streamlit as st
        token = st.secrets.get("GITHUB_PAT", "")
        owner = st.secrets.get("GITHUB_OWNER", "")
        repo  = st.secrets.get("GITHUB_REPO", "")
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            f"git+https://{token}@github.com/{owner}/{repo}.git",
            "--quiet"
        ], check=True)

