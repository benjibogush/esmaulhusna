# 📖 Esma-ul Husna (99 Names of Allah) PDF Generator  

Generate dynamicly arranged PDFs of the 99 Names of dear Allah ﷻ almighty with support for Arabic text rendering, transliterations, and translations.  

---

## 🚀 Quick Start  

# Clone the repository
git clone <repo>
cd <repo>

# Create and activate a virtual environment
python3 -m venv venv

# macOS / Linux
source venv/bin/activate  

# Windows (PowerShell / CMD)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python3 cli.py

---

## 🛠️ Dependencies  

- **reportlab** → PDF generation  
- **arabic-reshaper** + **python-bidi** → Proper Arabic text rendering  
- **pyinstaller** → Bundle into `.dmg` (macOS) or `.exe` (Windows)  

✅ Built-in modules already used (no need to list in `requirements.txt`):  
`logging`, `argparse`, `json`  

---

## 📌 Best Practice  

After every code change, update your dependency lock:  

pip freeze > requirements.txt

---

## ⚠️ Limitation  

Currently, executables can only be built **on the same OS as the target**:  
- Windows → `.exe`  
- macOS → `.dmg`  
- Linux → _(not yet integrated)_  

---

## 🔀 Cross-Platform Options : Pending, see issues

If you want to try cross-building:  

- 🐳 **Docker-based PyInstaller** – e.g. `cdrx/pyinstaller-windows` to build `.exe` from macOS/Linux.  
- ☁️ **GitHub Actions** – use hosted Windows/macOS runners to build for each OS.  
- 🍷 **Wine (experimental)** – build/test Windows executables from Linux/macOS.  

---

## 🧾 Legacy Instructions (macOS example)  

# Install manually
pip install reportlab arabic-reshaper python-bidi

# or
python3 -m pip install reportlab arabic-reshaper python-bidi

# or inside venv
python3 -m venv venv
source venv/bin/activate
pip install reportlab arabic-reshaper python-bidi

# Run the app
python3 ./app.py3

The generated file will be saved as:  
Esma_ul_Husna_99_Names_Of_Allah.pdf

# Exit virtual environment
deactivate

---

## ⚡ TODO: GitHub Release Build 

