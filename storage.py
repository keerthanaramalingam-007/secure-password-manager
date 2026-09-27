import json
import os

from crypto_utils import (
    generate_salt,
    encrypt_data,
    decrypt_data
)


DATA_FOLDER = "data"
VAULT_FILE = os.path.join(DATA_FOLDER, "vault.json")


def ensure_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)


def vault_exists():
    return os.path.exists(VAULT_FILE)


def create_vault(master_password):
    ensure_data_folder()

    salt = generate_salt()

    empty_vault = []

    json_data = json.dumps(empty_vault)

    encrypted_data = encrypt_data(
        json_data,
        master_password,
        salt
    )

    vault_data = {
        "salt": salt.hex(),
        "data": encrypted_data.decode("utf-8")
    }

    with open(VAULT_FILE, "w", encoding="utf-8") as file:
        json.dump(vault_data, file, indent=4)


def load_vault(master_password):
    if not vault_exists():
        raise FileNotFoundError("Vault does not exist.")

    with open(VAULT_FILE, "r", encoding="utf-8") as file:
        vault_data = json.load(file)

    salt = bytes.fromhex(vault_data["salt"])

    encrypted_data = vault_data["data"].encode("utf-8")

    decrypted_data = decrypt_data(
        encrypted_data,
        master_password,
        salt
    )

    return json.loads(decrypted_data)


def save_vault(entries, master_password):
    ensure_data_folder()

    with open(VAULT_FILE, "r", encoding="utf-8") as file:
        vault_data = json.load(file)

    salt = bytes.fromhex(vault_data["salt"])

    json_data = json.dumps(
        entries,
        indent=4
    )

    encrypted_data = encrypt_data(
        json_data,
        master_password,
        salt
    )

    vault_data["data"] = encrypted_data.decode("utf-8")

    with open(VAULT_FILE, "w", encoding="utf-8") as file:
        json.dump(vault_data, file, indent=4)