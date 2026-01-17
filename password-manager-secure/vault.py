import json
import os
import base64
from typing import Dict, Any

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


VAULT_FILE = "vault.enc"


def _b64e(data: bytes) -> str:
    """Base64-encode bytes -> string (so we can store bytes in JSON)."""
    return base64.b64encode(data).decode("utf-8")


def _b64d(data_str: str) -> bytes:
    """Base64-decode string -> bytes."""
    return base64.b64decode(data_str.encode("utf-8"))


def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Convert the user's master password into a 32-byte encryption key using scrypt.

    Why:
    - Users type passwords, not random 32-byte keys.
    - scrypt is a KDF (Key Derivation Function) designed to be slow and memory-hard,
      making brute force attacks harder.
    """
    if not isinstance(master_password, str) or master_password == "":
        raise ValueError("Master password must be a non-empty string.")

    # scrypt parameters: these are reasonable defaults for a local app.
    # You can tune them later depending on performance.
    kdf = Scrypt(
        salt=salt,
        length=32,      # 32 bytes = 256-bit key for AES
        n=2**14,        # CPU/memory cost parameter
        r=8,
        p=1,
    )

    return kdf.derive(master_password.encode("utf-8"))


def encrypt_vault(vault_data: Dict[str, Any], master_password: str) -> Dict[str, str]:
    """
    Encrypt the entire vault dictionary using AES-GCM.

    Returns a JSON-serializable dict containing:
    - salt (base64)
    - nonce (base64)
    - ciphertext (base64)
    """
    # 1) Random salt for key derivation
    salt = os.urandom(16)

    # 2) Derive key from master password + salt
    key = derive_key(master_password, salt)

    # 3) Encrypt using AES-GCM (authenticated encryption)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # AES-GCM standard nonce size is 12 bytes

    plaintext = json.dumps(vault_data).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    return {
        "version": "1",
        "kdf": "scrypt",
        "cipher": "aes-gcm",
        "salt": _b64e(salt),
        "nonce": _b64e(nonce),
        "ciphertext": _b64e(ciphertext),
    }


def decrypt_vault(payload: Dict[str, str], master_password: str) -> Dict[str, Any]:
    """
    Decrypt the vault payload using the master password.

    If the password is wrong OR the file is tampered with, AES-GCM will fail and
    we raise a ValueError.
    """
    try:
        salt = _b64d(payload["salt"])
        nonce = _b64d(payload["nonce"])
        ciphertext = _b64d(payload["ciphertext"])
    except KeyError as e:
        raise ValueError(f"Vault file is missing a required field: {e}") from e

    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except Exception as e:
        # Wrong password OR data modified
        raise ValueError("Unable to decrypt vault. Wrong master password or corrupted vault file.") from e

    return json.loads(plaintext.decode("utf-8"))


def load_vault(master_password: str) -> Dict[str, Any]:
    """
    Load and decrypt the vault from disk.

    - If vault file does not exist, return an empty vault structure.
    - If it exists, decrypt it with the provided master password.
    """
    if not os.path.exists(VAULT_FILE):
        # Empty vault structure (we can evolve this later)
        return {"items": []}

    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    return decrypt_vault(payload, master_password)


def save_vault(vault_data: Dict[str, Any], master_password: str) -> None:
    """
    Encrypt and save the vault to disk as a single file.
    """
    payload = encrypt_vault(vault_data, master_password)
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)
