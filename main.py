import sys
import os
import json
import re
import shutil
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
TYPOS_FILE = os.path.join(DIR, "typos.json")
BACKUP_DIR = os.path.join(DIR, "backups")
LOG_FILE = os.path.join(DIR, "log.txt")

os.makedirs(BACKUP_DIR, exist_ok=True)

def load_typos():
    with open(TYPOS_FILE, 'r') as f:
        return json.load(f)

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {msg}\n")

def backup_file(filepath):
    backup_name = os.path.basename(filepath) + f".{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(filepath, backup_path)
    return backup_path

def fix_python_file(filepath, dry_run=False, verbose=False):
    typos = load_typos()
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    for wrong, correct in typos.items():
        pattern = r'\b' + re.escape(wrong) + r'\b'
        if re.search(pattern, content):
            matches = len(re.findall(pattern, content))
            content = re.sub(pattern, correct, content)
            fixes.append(f"{wrong}->{correct}({matches}x)")
    
    if content != original:
        if verbose:
            print(f"  {'[DRY]' if dry_run else ''}Fix: {', '.join(fixes)}")
        
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            log(f"Fixed: {filepath} - {', '.join(fixes)}")
        
        return len(fixes)
    
    return 0

def scan_directory(path, dry_run=False, verbose=False, create_backup=False):
    fixed_total = 0
    files_total = 0
    
    if os.path.isfile(path):
        if path.endswith('.py'):
            if create_backup and not dry_run:
                backup_file(path)
            fixed = fix_python_file(path, dry_run, verbose)
            if fixed > 0:
                print(f"{'[DRY] ' if dry_run else ''}Fixed: {path} ({fixed} fixes)")
                fixed_total += fixed
                files_total += 1
    else:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ['venv', 'env', '.git', '__pycache__', 'node_modules']]
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    if create_backup and not dry_run:
                        backup_file(filepath)
                    fixed = fix_python_file(filepath, dry_run, verbose)
                    if fixed > 0:
                        print(f"{'[DRY] ' if dry_run else ''}Fixed: {filepath} ({fixed} fixes)")
                        fixed_total += fixed
                        files_total += 1
    
    print(f"\nTotal: {files_total} files changed, {fixed_total} fixes")
    return files_total, fixed_total

def main():
    args = sys.argv[1:]
    
    if len(args) == 0 or args[0] in ['-h', '--help']:
        print("Auto Correct by Nanda")
        print("")
        print("Usage:")
        print("  autoheal file.py")
        print("  autoheal folder/")
        print("  autoheal .")
        print("  autoheal file.py --dry-run")
        print("  autoheal file.py --backup")
        print("  autoheal file.py --verbose")
        return
    
    path = args[0]
    dry_run = '--dry-run' in args
    verbose = '--verbose' in args
    create_backup = '--backup' in args
    
    if not os.path.exists(path):
        print(f"Error: {path} tidak ditemukan")
        return
    
    if dry_run:
        print("DRY RUN MODE - tidak ada perubahan")
    
    scan_directory(path, dry_run, verbose, create_backup)

if __name__ == "__main__":
    main()
