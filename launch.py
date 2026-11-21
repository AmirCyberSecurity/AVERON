import subprocess
import webbrowser
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REQUIREMENTS = os.path.join(BASE_DIR, "requirements.txt")
MANAGE = os.path.join(BASE_DIR, "manage.py")
URL = "http://127.0.0.1:8000/"

def main():
    print("[*] Initializing application...")

    if not os.path.isfile(REQUIREMENTS):
        print("[!] requirements.txt not found.")
        sys.exit(1)

    if not os.path.isfile(MANAGE):
        print("[!] manage.py not found.")
        sys.exit(1)

    print("[*] Installing dependencies...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS],
            check=True,
            cwd=BASE_DIR
        )
    except subprocess.CalledProcessError:
        print("[!] Failed to install dependencies.")
        sys.exit(1)

    print("[+] Dependencies installed.")
    print("[*] Starting application...")

    try:
        subprocess.Popen(
            [sys.executable, MANAGE, "runserver"],
            cwd=BASE_DIR
        )
    except OSError as error:
        print(f"[!] Failed to launch application: {error}")
        sys.exit(1)

    print("[+] Application launched.")
    print("[*] Opening browser in 3 seconds...")

    time.sleep(3)
    webbrowser.open(URL)

    print(f"[+] Browser opened: {URL}")

if __name__ == "__main__":
    main()
