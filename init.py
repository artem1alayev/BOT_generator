import os
import sys
from pathlib import Path
import venv
import subprocess


VENV_DIR = Path(__file__).parent / "venv"
MAIN_SCRIPT = Path(__file__).parent / "main.py"

if sys.platform == "win32":
    python_bin = VENV_DIR / "Scripts" / "python.exe"
else:
    python_bin = VENV_DIR / "bin" / "python"


def initialize_venv():
    if sys.prefix == sys.base_prefix:
        if not VENV_DIR.exists():
          venv.create(VENV_DIR, with_pip=True)
        os.execv(str(python_bin), [str(python_bin)] + sys.argv)


initialize_venv()

indicator = VENV_DIR / ".installed"
if os.path.exists("requirements.txt") and not indicator.exists():
    subprocess.check_call([python_bin, "-m", "pip", "install", "-r", "requirements.txt"])
    indicator.touch()

os.execv(str(python_bin), [str(python_bin), str(MAIN_SCRIPT)] + sys.argv[1:])