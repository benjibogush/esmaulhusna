
# 🕌 Esma-ül Hüsna CLI Toolkit

This CLI tool generates styled PDFs for the 99 Names of Allah (basic or extended with references), and allows you to manage reference data with CRUD operations, JSON import/export, and automatic backups.  
It also supports bundling into standalone executables for **macOS (arm64)** and **Windows (.exe)**.

---

## ⚡ Quick Start

### 🔹 macOS (arm64)

Run:

```bash
	python3 cli.py --bundle --arch macos-arm64

 ```
 Produces a universal binary: dist/macos/esmaulhusna



### 🔹 Windows 
Run:

```bash
	python3 cli.py --bundle --arch windows

 ```
 Produces a standalone executable: dist/windows/esmaulhusna.exe

 ⚠️ Note: If you run --arch windows on macOS/Linux, PyInstaller will still produce a Unix binary, not a real .exe!


## ⚠️ Cross-Platform Bundling (Limitations & Workarounds)

PyInstaller **does not support cross-compilation by default**.  
That means if you build on macOS, you will only get a macOS binary; if you build on Windows, you will only get a Windows `.exe`.  

### Options for Building Windows `.exe` from macOS/Linux

1. **Recommended: Build on the Target Platform**  
   - Use a Windows machine, VM (VirtualBox, Parallels), or CI/CD pipeline with a Windows runner.  
   - This guarantees compatibility and avoids Wine-related issues.  

2. **Workaround: Use Wine**  
   Wine allows running Windows applications on macOS/Linux.  
   You can install a Windows Python interpreter and run PyInstaller through Wine.

   #### Steps (macOS Homebrew example)
   ```bash
   # Install Wine
   brew install --cask wine-stable

   # Verify Wine
   wine --version

   # Install Windows Python inside Wine
   wine msiexec /i python-3.x.x-amd64.exe

   # Use Wine to run PyInstaller with Windows Python
   wine "C:/path/to/python.exe" -m pip install pyinstaller
   wine "C:/path/to/python.exe" -m PyInstaller --onefile cli.py

   ```
## Try this in your local - untested, use at your own risk!

Run:

 ```bash
	docker run --rm -v "$(pwd):/src" cdrx/pyinstaller-windows "pyinstaller --onefile cli.py --name esmaulhusna"
 ```
→ Should produce esmaulhusna.exe inside dist/.

## Before obtaining esmaulhusna executable

| Feature                  | Example Usage                                     |
| ------------------------ | ------------------------------------------------- |
| Show help                | `python3 cli.py` or `python3 cli.py --help`       |
| 🔍 Get entry by ID       | `python3 cli.py --get 5`                          |
| ✏️ Update entry by ID    | `python3 cli.py --update 5`                       |
| ➕ Create new entry       | `python3 cli.py --create`                         |
| ❌ Delete entry by ID     | `python3 cli.py --delete 5`                       |
| 📜 List all references   | `python3 cli.py --list`                           |
| 💾 Backup reference file | `python3 cli.py --backup`                         |
| ♻️ Revert backup file    | `python3 cli.py --revert backups/filename.bak.py` |
| 📤 Export to JSON        | `python3 cli.py --export-json`                    |
| 📥 Import from JSON      | `python3 cli.py --import-json file.json`          |
| 📦 Bundle app            | `python3 cli.py --bundle --arch macos-arm64`      |
| 📄 Generate basic PDF    | `python3 cli.py --generate basic`                 |
| 📄 Generate extended PDF | `python3 cli.py --generate extended`              |


## After obtaining esmaulhusna executable 

### Create, Read, Update, and Delete (CRUD) Operations
esmaulhusna --create
esmaulhusna --list
esmaulhusna --get <ID>
esmaulhusna --update <ID>
esmaulhusna --delete <ID>
esmaulhusna --delete <ID> --force

### Backup and Versioning
esmaulhusna --backup
esmaulhusna --revert <FILE>

### Data Management
esmaulhusna --export-json
esmaulhusna --import-json <FILE>

### File Generation
esmaulhusna --generate {basic,extended}

### Bundling and Distribution
esmaulhusna --bundle
esmaulhusna --bundle --arch {macos-arm64,windows}


