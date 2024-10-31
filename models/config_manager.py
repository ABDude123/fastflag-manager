import json
import os
from typing import Dict, Any, Tuple
import winreg  # For Windows registry access
from pathlib import Path
from .flag_validator import FlagValidator

class ConfigManager:
    def __init__(self):
        self.active_flags: Dict[str, Any] = {}
        self.validator = FlagValidator()
        self.load_active_flags()
        
    def load_active_flags(self):
        """Load currently active FastFlags from the config file"""
        try:
            config_path = Path('data/active_flags.json')
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.active_flags = json.load(f)
        except Exception as e:
            print(f"Error loading active flags: {str(e)}")
            self.active_flags = {}
            
    def save_active_flags(self):
        """Save current FastFlag configuration"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/active_flags.json', 'w') as f:
                json.dump(self.active_flags, f, indent=4)
        except Exception as e:
            print(f"Error saving active flags: {str(e)}")
            
    def set_flag_value(self, flag_name: str, value: Any) -> Tuple[bool, str]:
        """Set a FastFlag value and validate it"""
        self.active_flags[flag_name] = value
        self.save_active_flags()
        success = self.apply_flags()
        
        if success:
            # Validate the flag
            is_working, message = self.validator.validate_flag(flag_name, str(value))
            if is_working:
                return True, "Flag applied and verified working"
            else:
                return False, f"Flag applied but may not be working: {message}"
        return False, "Failed to apply flag"
        
    def remove_flag(self, flag_name: str):
        """Remove a FastFlag from active configuration"""
        if flag_name in self.active_flags:
            del self.active_flags[flag_name]
            self.save_active_flags()
            self.apply_flags()
            
    def get_flag_value(self, flag_name: str) -> Any:
        """Get current value of a FastFlag"""
        return self.active_flags.get(flag_name)
    
    def apply_flags(self) -> bool:
        """Apply all active FastFlags to Roblox"""
        try:
            settings_path = self._get_client_settings_path()
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing settings
            settings = {}
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            
            # Update FastFlags
            if 'FFlagList' not in settings:
                settings['FFlagList'] = {}
            
            settings['FFlagList'].update(self.active_flags)
            
            # Save updated settings
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
                
            return True
        except Exception as e:
            print(f"Error applying flags: {str(e)}")
            return False
            
    def get_game_recommendations(self, game_name: str):
        """Get recommended flags for a specific game"""
        return self.validator.get_game_recommendations(game_name)
    
    def _get_client_settings_path(self) -> Path:
        """Get path to Roblox ClientSettings.json"""
        if os.name == 'darwin':  # macOS
            base = Path.home() / "Library" / "Application Support" / "Roblox"
            versions = [d for d in base.glob('version-*') if d.is_dir()]
            if not versions:
                raise FileNotFoundError("No Roblox installation found")
                
            latest = max(versions, key=lambda x: x.stat().st_mtime)
            return latest / "ClientSettings" / "ClientAppSettings.json"
        else:
            raise OSError("Unsupported operating system")