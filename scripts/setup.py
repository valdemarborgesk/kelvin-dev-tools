#!/usr/bin/env python3
"""Cross-platform setup for Kelvin Dev Tools.

Works on macOS, Linux, and Windows.

Finds the best compatible Python (>=3.9, <3.14) on the system.
If none is available, installs Python 3.13 automatically.

Usage:
    python3 scripts/setup.py        (macOS/Linux)
    python scripts/setup.py         (Windows)
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
VENV_DIR = REPO_ROOT / "venv"
VENV_BIN = VENV_DIR / ("Scripts" if IS_WINDOWS else "bin")
PIP = VENV_BIN / ("pip.exe" if IS_WINDOWS else "pip")
KELVIN = VENV_BIN / ("kelvin.exe" if IS_WINDOWS else "kelvin")

# SDK compatibility range
MIN_PYTHON = (3, 9)
MAX_PYTHON = (3, 14)  # exclusive — SDK requires <3.14


def find_compatible_python():
    """Find the best compatible Python on the system.

    Returns the path to a compatible Python executable, or None.
    Checks the running Python first, then searches for python3.13 down to python3.9.
    """
    # Check if the Python running this script is already compatible
    v = sys.version_info
    if MIN_PYTHON <= (v.major, v.minor) < MAX_PYTHON:
        print(f"  Python {v.major}.{v.minor} OK")
        return sys.executable

    print(f"  Python {v.major}.{v.minor} is not supported — version 3.9 or newer is needed.")
    print("  Searching for a compatible Python version...")

    # Search for specific versioned binaries, newest first
    candidates = []
    for minor in range(13, 8, -1):  # 3.13 down to 3.9
        if IS_WINDOWS:
            names = [f"python3.{minor}", f"python3{minor}", "py"]
        else:
            names = [f"python3.{minor}"]
        for name in names:
            path = shutil.which(name)
            if path:
                candidates.append((path, minor))

    # Also check Windows py launcher which can target specific versions
    if IS_WINDOWS:
        py = shutil.which("py")
        if py:
            for minor in range(13, 8, -1):
                try:
                    result = subprocess.run(
                        [py, f"-3.{minor}", "-c", "import sys; print(sys.executable)"],
                        capture_output=True, text=True, timeout=10,
                    )
                    if result.returncode == 0:
                        exe = result.stdout.strip()
                        if exe:
                            candidates.append((exe, minor))
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue

    # Verify candidates actually work and are the right version
    for path, expected_minor in candidates:
        try:
            result = subprocess.run(
                [path, "-c", "import sys; print(sys.version_info.major, sys.version_info.minor)"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                major, minor = map(int, result.stdout.strip().split())
                if MIN_PYTHON <= (major, minor) < MAX_PYTHON:
                    print(f"  Found Python {major}.{minor}.")
                    return path
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            continue

    return None


def install_python():
    """Install Python 3.13 and return the path to the executable."""
    target = "3.13"
    print(f"  Python not found — installing Python {target}...")

    if IS_MAC:
        if not shutil.which("brew"):
            print("ERROR: Homebrew is not installed.")
            print("  Install it from https://brew.sh, then run setup again.")
            sys.exit(1)
        print(f"  Installing Python {target} via Homebrew (this may take a few minutes)...")
        try:
            subprocess.run(["brew", "install", f"python@{target}"], check=True)
        except subprocess.CalledProcessError:
            print("ERROR: Python installation failed.")
            print("  Check your internet connection and try again, or download Python manually:")
            print("  https://www.python.org/downloads/")
            sys.exit(1)
        path = shutil.which(f"python{target}") or shutil.which(f"python@{target}")
        if not path:
            # Homebrew sometimes needs the full path
            brew_prefix = subprocess.run(
                ["brew", "--prefix", f"python@{target}"],
                capture_output=True, text=True,
            ).stdout.strip()
            candidate = Path(brew_prefix) / "bin" / f"python{target}"
            if candidate.exists():
                path = str(candidate)
        if path:
            print(f"  Python {target} installed.")
            return path
        print("ERROR: Python was installed but could not be found.")
        print("  Restart your terminal and run setup again.")
        sys.exit(1)

    elif IS_WINDOWS:
        # Use winget if available, otherwise fall back to manual install
        winget = shutil.which("winget")
        if winget:
            print(f"  Downloading and installing Python {target}...")
            result = subprocess.run(
                ["winget", "install", f"Python.Python.{target}", "--accept-source-agreements", "--accept-package-agreements"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                # winget installs python, find it
                path = shutil.which(f"python{target}") or shutil.which("python")
                # Also try the py launcher
                py = shutil.which("py")
                if py:
                    try:
                        r = subprocess.run(
                            [py, f"-{target}", "-c", "import sys; print(sys.executable)"],
                            capture_output=True, text=True, timeout=10,
                        )
                        if r.returncode == 0 and r.stdout.strip():
                            path = r.stdout.strip()
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        pass
                if path:
                    print(f"  Python {target} installed.")
                    return path
        print(f"ERROR: Could not install Python automatically.")
        print(f"  Please download Python {target} from https://www.python.org/downloads/")
        print("  After installing, run setup again.")
        sys.exit(1)

    else:
        # Linux
        print(f"ERROR: Python {target} is not installed.")
        print(f"  Install it with your package manager:")
        print(f"    Ubuntu/Debian:  sudo apt install python{target} python{target}-venv")
        print(f"    Fedora/RHEL:   sudo dnf install python{target}")
        print("  Then run setup again.")
        sys.exit(1)


def create_venv(python_exe):
    if VENV_DIR.exists():
        # Check if existing venv uses a compatible Python
        existing_python = VENV_BIN / ("python.exe" if IS_WINDOWS else "python")
        if existing_python.exists():
            try:
                result = subprocess.run(
                    [str(existing_python), "-c", "import sys; print(sys.version_info.major, sys.version_info.minor)"],
                    capture_output=True, text=True, timeout=10,
                )
                if result.returncode == 0:
                    major, minor = map(int, result.stdout.strip().split())
                    if MIN_PYTHON <= (major, minor) < MAX_PYTHON:
                        print(f"  Tools environment already set up.")
                        return
                    else:
                        print(f"  Tools environment needs updating...")
                        shutil.rmtree(VENV_DIR)
            except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
                pass
        else:
            print("  Tools environment looks damaged — rebuilding...")
            shutil.rmtree(VENV_DIR)

    print(f"  Setting up tools environment...")
    try:
        subprocess.run([python_exe, "-m", "venv", str(VENV_DIR)], check=True)
    except subprocess.CalledProcessError:
        print("ERROR: Could not set up the tools environment.")
        print("  Try running setup again. If it keeps failing, restart your terminal first.")
        sys.exit(1)


def install_deps():
    print("  Installing Kelvin packages...")
    try:
        subprocess.run([str(PIP), "install", "-q", "--upgrade", "pip"], check=True)
        req = REPO_ROOT / "requirements.txt"
        if req.exists():
            subprocess.run([str(PIP), "install", "-q", "-r", str(req)], check=True)
        else:
            print("  WARNING: Package list not found — some files may be missing from the download.")
    except subprocess.CalledProcessError:
        print("ERROR: Could not install required packages.")
        print("  Check your internet connection and try running setup again.")
        sys.exit(1)


def configure_windows_login():
    """Configure login credential storage on Windows.

    Windows Credential Manager limits stored values to 2560 bytes.
    Kelvin login tokens often exceed this, causing auth failures.
    This installs a file-based alternative with no size limit.
    """
    print("  Configuring login storage...")

    result = subprocess.run(
        [str(PIP), "install", "-q", "keyrings.alt"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("  WARNING: Login storage setup failed — you may see errors when logging in.")
        return

    appdata = os.environ.get("APPDATA", "")
    if not appdata:
        print("  WARNING: Could not configure login storage — you may see errors when logging in.")
        return

    cfg_dir = Path(appdata) / "Python Keyring"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = cfg_dir / "keyring.cfg"
    cfg_file.write_text(
        "[backend]\ndefault-keyring=keyrings.alt.file.PlaintextKeyring\n",
        encoding="utf-8",
    )
    print("  Login storage configured.")


def check_kelvin():
    try:
        result = subprocess.run(
            [str(KELVIN), "--version"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            ver = result.stdout.strip().splitlines()[0]
            print(f"  Kelvin: {ver}")
        else:
            print("  WARNING: Kelvin tools not found — try running setup again.")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  WARNING: Kelvin tools not found — try running setup again.")


def check_docs():
    docs = REPO_ROOT / "docs"
    if docs.is_dir():
        print("  Platform documentation: available")
    else:
        print("  WARNING: Platform documentation not found.")


def check_docker():
    if not shutil.which("docker"):
        print("  WARNING: Docker not found (needed for app build/test)")
        return
    try:
        result = subprocess.run(
            ["docker", "info"], capture_output=True, timeout=10,
        )
        if result.returncode == 0:
            print("  Docker: available")
        else:
            print("  WARNING: Docker is not running (needed for app build/test)")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  WARNING: Docker is not running (needed for app build/test)")


def main():
    print("=== Kelvin Dev Tools Setup ===")
    os.chdir(REPO_ROOT)

    python_exe = find_compatible_python()
    if not python_exe:
        python_exe = install_python()

    create_venv(python_exe)
    install_deps()
    if IS_WINDOWS:
        configure_windows_login()
    check_kelvin()
    check_docs()
    check_docker()

    if IS_WINDOWS:
        activate_cmd = f"  {VENV_BIN}\\activate"
    else:
        activate_cmd = f"  source {VENV_BIN}/activate"

    print()
    print("Setup complete! Next steps:")
    print(activate_cmd)
    print("  kelvin auth login https://<env-url>")
    print()
    print("See AGENTS.md for the full developer guide.")


if __name__ == "__main__":
    main()
