import aiohttp
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Tuple, Optional
import hashlib

class AutoUpdater:
    def __init__(self):
        self.current_version = "1.0.0"
        self.update_url = "https://api.example.com/updates/mac"
        self.updates_dir = Path("updates")
        self.updates_dir.mkdir(exist_ok=True)
        
    async def check_for_updates(self) -> Tuple[bool, Optional[str]]:
        """Check for available updates"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(RELEASE_CONFIG["update_server"]) as response:
                    if response.status == 200:
                        data = await response.json()
                        latest_version = data["tag_name"].lstrip('v')
                        if self._version_is_newer(latest_version):
                            download_url = f"{RELEASE_CONFIG['download_server']}/FastFlagManager.dmg"
                            return True, download_url
        except Exception as e:
            print(f"Update check failed: {e}")
        return False, None
        
    async def download_update(self, url: str) -> Optional[Path]:
        """Download update DMG"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        dmg_path = self.updates_dir / "update.dmg"
                        with open(dmg_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                        return dmg_path
        except Exception as e:
            print(f"Download failed: {e}")
        return None
        
    def install_update(self, dmg_path: Path) -> bool:
        """Install the update"""
        try:
            # Mount DMG
            mount_cmd = ['hdiutil', 'attach', str(dmg_path)]
            subprocess.run(mount_cmd, check=True)
            
            # Copy new app to Applications
            volume_path = Path("/Volumes/FastFlag Manager Installer")
            app_path = volume_path / "FastFlag Manager.app"
            copy_cmd = ['cp', '-R', str(app_path), '/Applications/']
            subprocess.run(copy_cmd, check=True)
            
            # Unmount DMG
            unmount_cmd = ['hdiutil', 'detach', str(volume_path)]
            subprocess.run(unmount_cmd, check=True)
            
            # Clean up
            dmg_path.unlink()
            
            return True
        except Exception as e:
            print(f"Installation failed: {e}")
            return False
            
    def _version_is_newer(self, version: str) -> bool:
        """Compare version numbers"""
        current = [int(x) for x in self.current_version.split('.')]
        new = [int(x) for x in version.split('.')]
        return new > current