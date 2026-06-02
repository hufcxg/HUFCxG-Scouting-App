import subprocess, sys
import streamlit as st

def _install_private():
    try:
        import hufcxg_scout
    except ImportError:
        token = st.secrets.get("GITHUB_PAT", "")
        owner = st.secrets.get("GITHUB_OWNER", "")
        repo  = st.secrets.get("GITHUB_REPO", "")
        
        if not all([token, owner, repo]):
            st.error("Missing one or more secrets: GITHUB_PAT, GITHUB_OWNER, GITHUB_REPO")
            st.stop()
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install",
            f"git+https://{token}@github.com/{owner}/{repo}.git",
            "--quiet", "--disable-pip-version-check"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            st.error(f"Package install failed:\n{result.stderr}")
            st.stop()

st.set_page_config(
    page_title="Football Scout",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

_install_private()

# ══════════════════════════════════════════════════════════════════════════════
# PASSWORD GATE
# ══════════════════════════════════════════════════════════════════════════════

def _check_password() -> bool:
    if st.session_state.get("authenticated"):
        return True

    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: #0e1117; }
        [data-testid="stSidebar"]          { display: none; }
        [data-testid="collapsedControl"]   { display: none; }
        h2, p { color: #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([3, 2, 3])
    with col:
        st.markdown("## hufcxg Scouting App")
        st.markdown("Enter the password to continue.")
        pwd = st.text_input("Password", type="password",
                            key="pwd_input", label_visibility="collapsed")
        if pwd:
            if pwd == st.secrets.get("APP_PASSWORD", ""):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    return False

if not _check_password():
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #0e1117; }
    [data-testid="stSidebar"]          { background: #161b22; }
    h1, h2, h3, p { color: #e2e8f0; }
    .nav-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .nav-card:hover { border-color: #58a6ff; }
    .nav-card .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .nav-card h3    { color: #e2e8f0; margin: 0.4rem 0 0.6rem; }
    .nav-card p     { color: #8b949e; font-size: 0.85rem; margin: 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("# Scouting + Statistics App")
st.markdown("Select a section to get started.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="nav-card">
        <div class="icon">📊</div>
        <h3>Player Statistics</h3>
        <p>Percentile ranks, radars, role scores, shot maps,
        similar players and scout notes
        for any player in the dataset.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Open Player Statistics →", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Player_Statistics.py")

with col2:
    st.markdown("""
    <div class="nav-card">
        <div class="icon">🔍</div>
        <h3>Scouting</h3>
        <p>Add players to the
        watchlist and track them through to Scouted then decide on
        Discard, Potential and Immediate.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Open Scouting →", use_container_width=True):
        st.switch_page("pages/2_Scouting.py")

st.markdown("---")
st.caption("Logged in · [Log out](#)", unsafe_allow_html=True)
if st.button("Log out", key="logout"):
    st.session_state["authenticated"] = False
    st.rerun()
