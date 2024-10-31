import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from config.release_config import RELEASE_CONFIG

def create_release_info():
    dmg_path = Path("dist/FastFlagManager-Installer.dmg")
    if not dmg_path.exists():
        raise FileNotFoundError("DMG file not found")
        
    # Calculate file hash
    sha256_hash = hashlib.sha256()
    with open(dmg_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            
    release_info = {
        "version": RELEASE_CONFIG["current_version"],
        "release_date": datetime.now().isoformat(),
        "download_url": f"{RELEASE_CONFIG['download_server']}/FastFlagManager-{RELEASE_CONFIG['current_version']}.dmg",
        "file_hash": sha256_hash.hexdigest(),
        "file_size": dmg_path.stat().st_size,
        "mirrors": RELEASE_CONFIG["backup_mirrors"],
        "minimum_os": "10.15",
        "release_notes": "Latest release of FastFlag Manager",
        "auto_update": True
    }
    
    # Save release info
    with open("dist/release_info.json", "w") as f:
        json.dump(release_info, f, indent=4)
        
    return release_info

def prepare_release():
    # Create release info
    release_info = create_release_info()
    
    # Create release directory structure
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # Copy DMG and release info
    os.system(f"cp dist/FastFlagManager-Installer.dmg 'release/FastFlagManager-{RELEASE_CONFIG['current_version']}.dmg'")
    os.system("cp dist/release_info.json release/")
    
    print(f"Release {RELEASE_CONFIG['current_version']} prepared successfully!")
    print(f"DMG Hash: {release_info['file_hash']}")

if __name__ == "__main__":
    prepare_release() 