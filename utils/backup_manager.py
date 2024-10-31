import json
from pathlib import Path
from datetime import datetime

class BackupManager:
    def __init__(self, config):
        self.config = config
        self.backup_dir = Path("backups")
        
    def create_backup(self, name=None):
        if not name:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_data = {
            "flags": self.config.active_flags,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
        backup_path = self.backup_dir / f"{name}.json"
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=4) 