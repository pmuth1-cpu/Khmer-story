import sys
import os

# Ensure the root directory is on Python path so all modules resolve
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from web_ui import app

# Vercel entrypoint expects 'app'
app.debug = False
