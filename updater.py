#!/usr/bin/env python3

import os
import subprocess
import sys
import pkg_resources

GITIGNORE_TEMPLATE = """# === Python ===
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# === Virtual environments ===
env/
venv/
.venv/

# === Environment variables ===
.env
*.env
secrets.txt

# === Data and private JSONs ===
data/
!data/__init__.py
*.db
*.sqlite
*.json
!data/example.json

# === Logs ===
*.log
logs/
data/logs/
*.tmp
*.bak

# === System ===
.DS_Store
Thumbs.db

# === IDE / Editor ===
.vscode/
.idea/
*.swp
*.swo

# === Build / Installer / Cache ===
dist/
build/
__dist__/
*.egg-info/
*.spec
.installer_cache/

# === Compiled files ===
*.cpython-*
*.so

# === OS / Misc ===
*.orig
*.rej
"""


class WiseacreUpdater:
    def __init__(self):
        self.repo_path = os.getcwd()
        self.required_python = (3, 8)
        self.required_packages = {
            "python-telegram-bot": "20.7",
            "cryptography": "41.0.0",
            "python-dotenv": "1.0.0",
            "requests": "2.31.0"
        }

    def run_command(self, command, description):
        print(f"Running: {description}...")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            if result.returncode == 0:
                print(f"Success: {description}")
                return True, result.stdout
            else:
                print(f"Failed: {description} - {result.stderr}")
                return False, result.stderr
        except Exception as e:
            print(f"Error during {description}: {e}")
            return False, str(e)

    def check_python_version(self):
        print("Checking Python version...")
        current_version = (sys.version_info.major, sys.version_info.minor)
        if current_version < self.required_python:
            print(
                f"Error: Python {self.required_python[0]}.{self.required_python[1]}+ required "
                f"(current: {current_version[0]}.{current_version[1]})"
            )
            return False
        print(
            f"Python {current_version[0]}.{current_version[1]} "
            f"(required: {self.required_python[0]}.{self.required_python[1]}+)"
        )
        return True

    def check_git_status(self):
        print("Checking repository status...")
        success, local_commit = self.run_command("git rev-parse HEAD", "Getting local commit")
        if not success:
            return False
        success, remote_commit = self.run_command("git ls-remote origin HEAD | cut -f1", "Getting remote commit")
        if not success:
            return False
        if local_commit.strip() == remote_commit.strip():
            print("Local files are up to date")
            return True
        print("Updates found in repository")
        return False

    def update_repository(self):
        print("Updating repository...")
        self.run_command("git stash", "Saving local changes")
        success, _ = self.run_command("git pull --rebase", "Pulling updates")
        self.run_command("git stash pop", "Restoring local changes")
        return success

    def check_and_update_packages(self):
        print("Checking packages...")
        for package, required_ver in self.required_packages.items():
            try:
                installed_ver = pkg_resources.get_distribution(package).version
                if self.compare_versions(installed_ver, required_ver) < 0:
                    print(f"Updating {package} {installed_ver} -> {required_ver}")
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", f"{package}>={required_ver}"],
                        check=True
                    )
                else:
                    print(f"Package {package} {installed_ver} (up to date)")
            except pkg_resources.DistributionNotFound:
                print(f"Installing {package} {required_ver}")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", f"{package}>={required_ver}"],
                    check=True
                )
            except Exception as e:
                print(f"Error with {package}: {e}")

    def compare_versions(self, ver1, ver2):
        v1_parts = list(map(int, ver1.split(".")))
        v2_parts = list(map(int, ver2.split(".")))
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            if v1_part < v2_part:
                return -1
            elif v1_part > v2_part:
                return 1
        return 0

    def install_requirements(self):
        if os.path.exists("requirements.txt"):
            print("Installing dependencies from requirements.txt...")
            self.run_command("pip install -r requirements.txt", "Installing dependencies")

    def ensure_gitignore(self):
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w", encoding="utf-8") as f:
                f.write(GITIGNORE_TEMPLATE.strip() + "\n")
            print("[+] Created .gitignore file")
        else:
            print("[=] .gitignore already exists")

    def run(self):
        print("Starting WISEACRE Auto-Updater...")
        print(f"Working directory: {self.repo_path}")

        if not os.path.exists(".git"):
            print("Error: This is not a git repository")
            return False

        self.ensure_gitignore()

        if not self.check_python_version():
            return False

        needs_update = not self.check_git_status()
        if needs_update:
            if not self.update_repository():
                return False

        self.check_and_update_packages()
        self.install_requirements()

        print("WISEACRE is fully updated and ready to use!")
        return True


if __name__ == "__main__":
    updater = WiseacreUpdater()
    success = updater.run()
    sys.exit(0 if success else 1)
