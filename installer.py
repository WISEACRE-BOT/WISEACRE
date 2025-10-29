import os
import subprocess
import sys

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

ENV_TEMPLATE = """# Environment variables for WISEACRE
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
"""

REQUIREMENTS_FILE = "requirements.txt"


def create_file_if_missing(path: str, content: str):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"[+] Создан файл: {path}")
    else:
        print(f"[=] Найден существующий файл: {path}")


def install_requirements():
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"[!] Файл {REQUIREMENTS_FILE} не найден, установка пропущена.")
        return
    print("[*] Устанавливаю зависимости из requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])


def main():
    print("🔧 Установка проекта WISEACRE...\n")

    create_file_if_missing(".gitignore", GITIGNORE_TEMPLATE)
    create_file_if_missing(".env", ENV_TEMPLATE)

    os.makedirs("data", exist_ok=True)
    print("[=] Проверена директория data/")

    install_requirements()

    print("\n✅ Установка завершена. Теперь можно запустить бота командой:")
    print("   python bot.py\n")


if __name__ == "__main__":
    main()
