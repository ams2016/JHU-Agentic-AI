# Password Manager (Secure Local Version)

Local-only password manager using an encrypted vault and a simple UI.

## Security model
- Runs locally only
- Vault is encrypted at rest
- Master password is never stored

## Run
```bash
cd password-manager-secure
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
