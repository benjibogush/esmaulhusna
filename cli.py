import argparse
import logging
import shutil
import sys
import os
from datetime import datetime
import subprocess
import json

from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

REFERENCE_FILE = 'reference99names.py'
BACKUP_FILE = "reference99names.bak.py"
BACKUP_DIR = 'backups'

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def backup_reference(force=False):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"reference99names_{timestamp}.bak")
    if os.path.exists(REFERENCE_FILE):
        shutil.copy2(REFERENCE_FILE, backup_file)
        logging.info(f"✅ Backup created at: {backup_file}")
    elif not force:
        logging.warning("⚠️ No reference file found to back up.")
    return backup_file

def backup_reference_file():
    if not os.path.exists(BACKUP_FILE):
        shutil.copyfile(REFERENCE_FILE, BACKUP_FILE)
        logging.info(f"📦 Backup saved as: {BACKUP_FILE}")
    else:
        logging.info(f"📦 Backup already exists: {BACKUP_FILE}")

def save_references_to_file(data):
    with open(REFERENCE_FILE, "w", encoding="utf-8") as f:
        f.write("table_data = [\n")
        for entry in data:
            f.write(f"    {repr(entry)},\n")
        f.write("]\n")
    logging.info("💾 Saved updated references to file.")

def export_to_json():
    from reference99names import table_data
    output_file = "reference_export.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(table_data, f, ensure_ascii=False, indent=2)
    logging.info(f"📤 Exported reference data to {output_file}")

def import_from_json(json_path, force=False):
    if not os.path.isfile(json_path):
        logging.error("❌ JSON file does not exist.")
        return
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            new_data = json.load(f)

        if not isinstance(new_data, list):
            logging.error("❌ Invalid JSON format. Expected a list of entries.")
            return

        required_keys = {"Name_Arabic", "Name_English", "Description_Turkish", "Description_English"}
        for entry in new_data:
            if not required_keys.issubset(entry):
                logging.error("❌ One or more entries missing required keys.")
                return

        if force or input("Confirm import and overwrite? (y/n): ").lower() == "y":
            backup_reference_file()
            save_references_to_file(new_data)
            logging.info("✅ References imported from JSON.")
        else:
            logging.info("❌ Import cancelled by user.")
    except Exception as e:
        logging.error(f"❌ Failed to import JSON: {e}")

def validate_id(id_str):
    try:
        id_val = int(id_str)
        if id_val <= 0:
            raise ValueError("ID must be a positive integer.")
        return id_val
    except ValueError:
        logging.error("❌ Invalid ID. Please enter a positive number.")
        return None

def validate_unique_id(new_id, table_data):
    if any(str(entry.get("id")) == str(new_id) for entry in table_data):
        logging.error(f"❌ ID {new_id} already exists.")
        return False
    return True

def is_running_in_bundle():
    return getattr(sys, 'frozen', False)

def resolve_script_path(filename):
    base_path = sys._MEIPASS if is_running_in_bundle() else os.path.abspath('.')
    return os.path.join(base_path, filename)    

def resource_path(relative_path):
    # Support PyInstaller bundle path or normal dev path
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

font_path = resource_path("DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont('DejaVu', font_path))


def bundle_app(arch, force=False):
    system = platform.system().lower()
    if arch == "windows" and system != "windows":
        logging.error("🚫 Cannot build Windows .exe from macOS. Please run this on a Windows machine or use a VM/Docker.")
        return
    if arch == "macos-arm64" and system != "Darwin":
        logging.error("🚫 macOS ARM build must be run on macOS ARM.")
        return

    if not arch:
        logging.error("❌ Architecture must be specified with --arch")
        return
    if not shutil.which("pyinstaller"):
        logging.error("❌ PyInstaller not found. Install it using: pip install pyinstaller")
        return

    datas = [
        "--add-data=reference99names.py:.",
        "--add-data=app_basic.py:.",
        "--add-data=app_detailed.py:.",
        "--add-data=basic_reference_helper.py:.",
        "--add-data=DejaVuSans.ttf:.",
        "--add-data=Amiri-Regular.ttf:.",
        "--add-data=helper.py:.",
        "--add-data=readme_bundle.md:.",
        "--add-data=readme.md:."
    ]

    hidden_imports = [
        "--hidden-import=reportlab.rl_config",
        "--hidden-import=reportlab.graphics",
        "--hidden-import=json"
        "--hidden-import=bidi.algorithm"
        "--hidden-import=arabic_reshaper"
    ]

    logging.info(f"📦 Bundling CLI app for {arch}...")

    output_dir = os.path.join("dist", arch)
    os.makedirs(output_dir, exist_ok=True)

    # for distpath, put build in dist/macos-arm64
    # if arch preferred within executable name, "--name", f"esmaulhusna_{arch}",
    cmd = [
        "pyinstaller",
        "--onefile",
        "--clean",
        "--distpath", output_dir,   
        "--name", "esmaulhusna",
        *datas,
        *hidden_imports,
        "cli.py"
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Bundling failed: {e}")
        return

    logging.info("✅ CLI app bundled successfully.")


def main():
    parser = argparse.ArgumentParser(description="🕌 Esma-ül Hüsna CLI Toolkit")

    parser.add_argument("--backup", action="store_true", help="Create a backup of the reference file")
    parser.add_argument("--revert", metavar="FILE", help="Revert reference file from given backup")
    parser.add_argument("--bundle", action="store_true", help="Bundle the CLI into a standalone executable")
    parser.add_argument("--arch", choices=["macos-arm64", "windows"], help="Target architecture for bundling")
    parser.add_argument("--force", action="store_true", help="Force action without prompt")
    parser.add_argument("--list", action="store_true", help="List all reference entries")
    parser.add_argument("--get", type=str, help="Get a specific reference by ID")
    parser.add_argument("--update", type=str, help="Update a reference by ID")
    parser.add_argument("--delete", type=str, help="Delete a reference by ID")
    parser.add_argument("--create", action="store_true", help="Create a new reference")
    parser.add_argument("--generate", choices=["basic", "extended"], help="Generate PDF file")
    parser.add_argument("--export-json", action="store_true", help="Export all references to JSON")
    parser.add_argument("--import-json", metavar="FILE", help="Import reference data from JSON file")

    args = parser.parse_args()

    # Print help if nothing was provided
    if not vars(args):
        parser.print_help()
        return

    if args.backup:
        backup_reference(force=args.force)

    elif args.revert:
        if not os.path.isfile(args.revert):
            logging.error("❌ Backup file does not exist.")
            return
        shutil.copy2(args.revert, REFERENCE_FILE)
        logging.info(f"✅ Reference file reverted from: {args.revert}")

    elif args.bundle:
        bundle_app(args.arch, force=args.force)

    elif args.list:
        list_references()

    elif args.get:
        get_reference_by_id(args.get)

    elif args.update:
        update_reference_by_id(args.update, force=args.force)

    elif args.delete:
        delete_reference_by_id(args.delete, force=args.force)

    elif args.create:
        create_reference(force=args.force)

    elif args.generate == "basic":
        import runpy
        logging.info("📄 Generating basic PDF...")
        runpy.run_path(resolve_script_path("app_basic.py"), run_name="__main__")
        logging.info("✅ Basic PDF generated.")

    elif args.generate == "extended":
        import runpy
        logging.info("📄 Generating extended PDF with references...")
        runpy.run_path(resolve_script_path("app_detailed.py"), run_name="__main__")
        logging.info("✅ Extended PDF generated.")

    elif args.export_json:
        export_to_json()

    elif args.import_json:
        import_from_json(args.import_json, force=args.force)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
