# 🐳 Docker Images Manager

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-brightgreen.svg)
![Bash](https://img.shields.io/badge/bash-5.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Backup and restore Docker images with style! 💎✨**

</div>

---

## ✨ Features

- 💾 **Save** Docker images to TAR files
- 📥 **Load** TAR files back to Docker
- 📦 **List** images and backups with details
- 🗑️ **Delete** old backups safely
- 🎨 **Beautiful** colorful terminal UI
- 🔄 **Loop Mode** - continuous operations (Python)
- 🔢 **Smart Selection** - ranges like `1,3-5`

---

## 🚀 Quick Start

```bash
# Download
git clone https://github.com/your-repo/docker-manager.git
cd docker-manager

# Choose your version:

# Python (Windows/Linux/macOS)
python docker_Images_backup.py

# Bash (Linux/macOS)
chmod +x docker_Images_backup.sh
./docker_Images_backup.sh
```

### 🎯 Menu Options

```
1) 💾 Save images (all or specific)
2) 📥 Load images (all or specific)
3) 📦 List Docker images
4) 📚 List TAR backups
5) 🗑️  Delete backups
6) 📚 Help
7) 🚪 Exit
```

**Select with ranges:** `1,3-5` or `1,2,4`

---

## 🐍 vs 🐚 Which Version?

| Feature | Python 🐍 | Bash 🐚 |
|---------|-----------|---------|
| **Platform** | Windows/Linux/macOS | Linux/macOS |
| **UI** | Box borders ╔═══╗ | Classic colors |
| **Loop Mode** | ✅ Infinite | ❌ Single run |
| **Safety** | Type 'YES' | Type 'Y' |
| **Progress** | `[1/5]` counters | Basic |
| **File Sizes** | Shows MB | No |

**💡 Recommendation:**
- Windows? → Python
- Want loop mode? → Python
- Shell purist? → Bash

---

## 📸 Preview

### Python Version
```
════════════════════════════════════════════════════════════
                 🐳 DOCKER IMAGES MANAGER 🐳
                   ✨ Super Cool Edition ✨
════════════════════════════════════════════════════════════

🔍 Checking Docker...
   ✅ Docker is installed
   ✅ Docker daemon is running

📋 MAIN MENU
────────────────────────────────────────────────────────────
  1) 💾 Save Docker images
  2) 📥 Load Docker images
  ...
```

### Bash Version
```
============================================
🐳 Docker Images Manager - Super Cool Edition! 🚀
============================================

1) 💾 Save Docker images (All or Specific)
2) 📦 Load tar files as Docker images
...
```

---

## 📁 File Structure

```
docker-manager/
├── docker_Images_backup.py    # Python v3.0
├── docker_Images_backup.sh    # Bash v2.0
└── backups/                    # Auto-created
    ├── nginx_latest.tar
    ├── postgres_13.tar
    └── redis_alpine.tar
```

---

## 🔧 Requirements

- Docker Desktop installed and running
- Python 3.6+ (for Python version)
- Bash 5.0+ (for Bash version)

---

<div align="center">

**Made with 💙 by AI**

⭐ **Star if helpful!** ⭐

</div>
