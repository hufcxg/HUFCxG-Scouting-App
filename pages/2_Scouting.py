#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess, sys, os
import streamlit as st

def ensure_installed():
    try:
        from hufcxg_scout.pages.scouting import run
    except (ImportError, ModuleNotFoundError):
        token = st.secrets.get("GITHUB_PAT", "")
        owner = st.secrets.get("GITHUB_OWNER", "")
        repo  = st.secrets.get("GITHUB_REPO", "")

        install_dir = "/tmp/hufcxg_packages"
        os.makedirs(install_dir, exist_ok=True)

        result = subprocess.run([
            sys.executable, "-m", "pip", "install",
            f"git+https://{token}@github.com/{owner}/{repo}.git",
            "--target", install_dir,
            "--quiet", "--disable-pip-version-check",
            "--upgrade",
        ], capture_output=True, text=True)

        if result.returncode != 0:
            st.error(f"Package install failed:\n{result.stderr}")
            st.stop()

        if install_dir not in sys.path:
            sys.path.insert(0, install_dir)

ensure_installed()

from hufcxg_scout.pages.scouting import run
run()
