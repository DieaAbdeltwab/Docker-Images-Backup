# 🐳 Docker Images Backup Manager

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bash](https://img.shields.io/badge/Bash-5.0+-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>


**A simple tool to backup and restore Docker images**

---

## 📋 Features

- 💾 Save Docker images to TAR files
- 📥 Load TAR files back to Docker
- 📦 List Docker images and backups
- 🗑️ Delete old backup files
- 🎨 Colorful terminal interface
- 🔢 Smart selection (ranges like `1,3-5`)

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/DieaAbdeltwab/Docker-Images-Backup.git
cd Docker-Images-Backup

# Run Python version (recommended for Windows)
python docker_Images_backup.py

# OR run Bash version (Linux/macOS only)
chmod +x docker_Images_backup.sh
./docker_Images_backup.sh
```

---

## 🎯 Menu Options

```
1) 💾 Save Docker images (All or Specific)
2) 📥 Load Docker images (All or Specific)
3) 📦 List Docker images
4) 📚 List TAR backup files
5) 🗑️ Delete backup files
6) 📚 Help
7) 🚪 Exit
```

---

## 🐍 Python vs 🐚 Bash

| Feature | Python | Bash |
|---------|--------|------|
| **Windows Support** | ✅ | ❌ |
| **Loop Mode** | ✅ | ❌ |
| **File Sizes** | ✅ | ❌ |
| **Progress Counters** | ✅ | ❌ |
| **Linux/macOS** | ✅ | ✅ |

**Recommendation:** Use Python version for better features and cross-platform support.

---

## 📖 Usage Examples

### Backup All Images
```bash
# Select option 1
# Choose 'all'
# All images saved to ./backups/ folder
```

### Restore Specific Images
```bash
# Select option 2
# Enter: 1,3-5 (loads images 1, 3, 4, and 5)
```

### Delete Old Backups
```bash
# Select option 5
# Enter numbers or ranges
# Confirm deletion
```

---

## 🔧 Requirements

- Docker installed and running
- Python 3.6+ (for Python version)
- Bash 5.0+ (for Bash version)

---

## 📁 File Structure

```
Docker-Images-Backup/
├── docker_Images_backup.py    # Python version
├── docker_Images_backup.sh    # Bash version
└── backups/                    # Auto-created
    ├── nginx_latest.tar
    └── postgres_13.tar
```

---
<div align="center">

## 👤 Author

**Diea AbdelTawab**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dieaabdeltwab/)

</div>

---

⭐ **Star this repo if it helped you!**
