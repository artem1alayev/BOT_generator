import os
import sys
from pathlib import Path
import venv



VENV_DIR = Path(__file__).parent / "venv"


def initialize_venv():
    if sys.prefix == sys.base_prefix:
        if not VENV_DIR.exists():
          venv.create(VENV_DIR, with_pip=True)
        if sys.platform == "win32":
            os.execv(str(VENV_DIR / "Scripts" / "python.exe"), [str(VENV_DIR / "Scripts" / "python.exe")] + sys.argv)
        else:
            os.execv(str(VENV_DIR / "bin" / "python"), [str(VENV_DIR / "bin" / "python")] + sys.argv)


initialize_venv()



