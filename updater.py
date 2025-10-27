#!/usr/bin/env python3

import os
import subprocess
import sys
import pkg_resources
from packaging import version

class WiseacreUpdater:
    def __init__(self):
        self.repo_path = os.getcwd()
        self.required_python = "3.8"
        self.required_packages = {
            "python-telegram-bot": "20.7",
            "cryptography": "41.0.0", 
            "python-dotenv": "1.0.0",
            "requests": "2.31.0"
        }

    def run_command(self, command, description):
        print(f"Running: {description}...")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                                 text=True, cwd=self.repo_path)
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
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        if version.parse(current_version) < version.parse(self.required_python):
            print(f"Error: Python {self.required_python}+ required (current: {current_version})")
            return False
        else:
            print(f"Python {current_version} (required: {self.required_python}+)")
            return True

    def check_git_status(self):
        print("Checking repository status...")
        
        success, local_commit = self.run_command(
            "git rev-parse HEAD", "Getting local commit"
        )
        if not success:
            return False
            
        success, remote_commit = self.run_command(
            "git ls-remote origin HEAD | cut -f1", "Getting remote commit"
        )
        if not success:
            return False
            
        if local_commit.strip() == remote_commit.strip():
            print("Local files are up to date")
            return True
        else:
            print("Updates found in repository")
            return False

    def update_repository(self):
        print("Updating repository...")
        
        self.run_command("git stash", "Saving local changes")
        
        success, output = self.run_command("git pull --rebase", "Pulling updates")
        
        self.run_command("git stash pop", "Restoring local changes")
        
        return success

    def check_and_update_packages(self):
        print("Checking packages...")
        
        for package, required_ver in self.required_packages.items():
            try:
                installed_ver = pkg_resources.get_distribution(package).version
                if version.parse(installed_ver) < version.parse(required_ver):
                    print(f"Updating {package} {installed_ver} -> {required_ver}")
                    subprocess.run([sys.executable, "-m", "pip", "install", 
                                  f"{package}>={required_ver}"], check=True)
                else:
                    print(f"Package {package} {installed_ver} (up to date)")
            except pkg_resources.DistributionNotFound:
                print(f"Installing {package} {required_ver}")
                subprocess.run([sys.executable, "-m", "pip", "install", 
                              f"{package}>={required_ver}"], check=True)
            except Exception as e:
                print(f"Error with {package}: {e}")

    def install_requirements(self):
        if os.path.exists("requirements.txt"):
            print("Installing dependencies from requirements.txt...")
            self.run_command("pip install -r requirements.txt", "Installing dependencies")

    def run(self):
        print("Starting WISEACRE Auto-Updater...")
        print(f"Working directory: {self.repo_path}")
        
        if not os.path.exists(".git"):
            print("Error: This is not a git repository")
            return False
        
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
