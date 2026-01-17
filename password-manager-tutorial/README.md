# Password Manager (Tutorial Version)

CLI-based password manager built as part of a guided Python exercise.

## Features
- Master login (UID + password)
- Add / Retrieve / Update / Delete passwords per user
- Secure password generation using Python `secrets`
- JSON storage and timestamped logging

## Run Locally
1. Clone the repo
2. In `password-manager-tutorial/`, create local data files:
   - Copy `master_login.sample.json` → `master_login.json`
   - Copy `app_password.sample.json` → `app_password.json`
3. Run:
```bash
python3 password_manager.py


