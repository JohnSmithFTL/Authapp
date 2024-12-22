# config.py
import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent

# Database settings
DB_PATH = os.path.join(BASE_DIR, 'users.xlsx')

# Page settings
PAGES_DIR = os.path.join(BASE_DIR, 'pages')

# Application settings
APP_SETTINGS = {
    'page_title': 'My Streamlit App',
    'page_icon': '🚀',
    'layout': 'wide',
    'initial_sidebar_state': 'auto'
}

# Style settings
STYLE = """
<style>
    .stButton button {
        width: 100%;
    }
    .stTextInput input {
        width: 100%;
    }
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: center;
    }
</style>
"""
