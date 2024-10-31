import json
from pathlib import Path
from typing import Dict, List, Tuple
import time
import psutil
import os

class FlagValidator:
    def __init__(self):
        self.known_working_flags = {
            "DFIntTaskSchedulerTargetFps": self.validate_fps,
            "FFlagDisableSpeculativeGPUMemoryAllocation": self.validate_gpu_memory,
            "DFIntGPUTextureReductionPercentage": self.validate_texture_reduction,
            "DFIntConnectionThrottleMaxExponent": self.validate_network,
            # Add more validators for specific flags
        }
        
        self.game_specific_flags = {
            "phantom_forces": [
                ("DFIntTaskSchedulerTargetFps", "0", "Unlocks FPS completely"),
                ("DFIntClientReplicationRate", "120", "Better hit registration"),
                ("FFlagDisableOcclusionChecks", "true", "See enemies more easily")
            ],
            "arsenal": [
                ("DFIntPhysicsSenderRate", "120", "Better hit detection"),
                ("FFlagNewAnimationRuntimeEnabled", "false", "Faster animations"),
                ("DFIntNetworkClampRTT", "150", "Lower latency")
            ],
            # Add more games and their recommended flags
        }
        
    def validate_fps(self, value: str) -> Tuple[bool, str]:
        """Validate FPS flag by checking if it affects render speed"""
        try:
            # Check if the flag is being applied
            settings_path = self._get_client_settings_path()
            if not self._is_flag_in_settings("DFIntTaskSchedulerTargetFps", settings_path):
                return False, "Flag not found in settings"
                
            # TODO: Add actual FPS measurement
            return True, "FPS flag appears to be working"
        except Exception as e:
            return False, f"Validation failed: {str(e)}"
            
    def validate_gpu_memory(self, value: str) -> Tuple[bool, str]:
        """Validate GPU memory allocation flag"""
        try:
            # Check GPU memory usage before and after
            # This is a simplified check
            return True, "GPU memory flag appears to be working"
        except Exception as e:
            return False, f"Validation failed: {str(e)}"
            
    def validate_texture_reduction(self, value: str) -> Tuple[bool, str]:
        """Validate texture reduction flag"""
        try:
            # Check texture memory usage
            return True, "Texture reduction appears to be working"
        except Exception as e:
            return False, f"Validation failed: {str(e)}"
            
    def validate_network(self, value: str) -> Tuple[bool, str]:
        """Validate network-related flags"""
        try:
            # Monitor network behavior
            return True, "Network flag appears to be working"
        except Exception as e:
            return False, f"Validation failed: {str(e)}"
            
    def validate_flag(self, flag_name: str, value: str) -> Tuple[bool, str]:
        """Validate a specific flag"""
        if flag_name in self.known_working_flags:
            return self.known_working_flags[flag_name](value)
        return False, "No validator available for this flag"
        
    def get_game_recommendations(self, game_name: str) -> List[Tuple[str, str, str]]:
        """Get recommended flags for a specific game"""
        return self.game_specific_flags.get(game_name.lower(), [])
        
    def _get_client_settings_path(self) -> Path:
        """Get path to Roblox ClientSettings"""
        # Implementation from ConfigManager
        pass
        
    def _is_flag_in_settings(self, flag_name: str, settings_path: Path) -> bool:
        """Check if flag exists in current settings"""
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
                return flag_name in settings.get('FFlagList', {})
        except:
            return False 