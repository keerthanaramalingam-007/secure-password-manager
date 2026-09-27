# 🔐 Secure Password Manager

A local password manager developed using Python that securely stores user credentials in an encrypted JSON vault.

## 📌 Project Overview

The Secure Password Manager is a local desktop application designed to safely store and manage passwords and account credentials.

The application uses a master password to protect the vault and encrypts the stored credentials before writing them to disk.


## ✨ Features

* 🔐 Master password authentication
* 🔒 Encrypted local credential storage
* 🔑 Scrypt-based key derivation
* 🛡️ Fernet authenticated encryption
* ➕ Add credentials
* ✏️ Edit credentials
* 👁️ Show/hide passwords
* 🔎 Search credentials
* 🗑️ Delete credentials
* 🎲 Secure password generator
* 📊 Password strength indicator
* 📋 Secure clipboard handling
* ⏱️ Automatic vault locking
* 🔒 Manual vault locking
* 💾 Local encrypted JSON storage
* 🌐 No cloud storage or external API required


* Secure master password authentication
* Encrypted local password storage
* Add new credentials
* Retrieve saved passwords
* Search credentials
* Delete credentials
* Secure password generator
* Local encrypted JSON vault
* Lock and unlock functionality
* No cloud storage or external API required

## 🛠️ Technologies Used

* Python
* Tkinter
* Cryptography
* Fernet encryption
* Scrypt Key Derivation Function
* JSON

## 🔐 Security

The application does not store the master password directly.

The master password is used with the Scrypt key derivation function to derive an encryption key. The credentials are then encrypted using Fernet authenticated encryption before being stored in the local vault.

### Security Flow

Master Password
↓
Scrypt Key Derivation
↓
Encryption Key
↓
Fernet Encryption
↓
Encrypted JSON Vault

## 📁 Project Structure

```text
Password_Manager/
│
├── main.py
├── crypto_utils.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── screenshots/
│
└── data/
    └── vault.json
```

## ⚙️ Installation

### 1. Clone or download the project

Open the project folder in a terminal.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

## 🚀 How to Use

### First-time setup

1. Launch the application.
2. Create a master password.
3. Confirm the master password.
4. Create the secure vault.

### Add a credential

1. Click **Add Password**.
2. Enter the website or service.
3. Enter the username or email.
4. Enter the password.
5. Click **Save Credential**.

### Search

Enter a website or username in the search box.

### Retrieve

Select an account and click **View Password**.

### Delete

Select an account and click **Delete**.

### Lock

Click **Lock** to return to the master-password screen.

## 🧪 Testing

The following functions were tested:

* Master password creation
* Master password verification
* Incorrect password rejection
* Credential addition
* Credential retrieval
* Credential search
* Credential deletion
* Vault locking
* Vault reopening
* Encrypted local storage

## 🔮 Future Enhancements

* Edit existing credentials
* Password strength meter
* Automatic vault locking
* Improved GUI
* Clipboard auto-clear
* Backup and restore functionality
* Two-factor authentication
* More advanced password-generation options

## 👨‍💻 Project Type

Cybersecurity / Python Desktop Application

## 📄 License

This project was created for educational and internship purposes.





















