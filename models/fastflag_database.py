import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import os

@dataclass
class FastFlag:
    name: str
    description: str
    default_value: any
    value_type: str
    category: str
    exploitable: bool = False
    exploit_description: Optional[str] = None
    
    def validate_value(self, value: Any) -> bool:
        """Validate if a value is appropriate for this flag"""
        try:
            if self.value_type == "int":
                int(value)
            elif self.value_type == "float":
                float(value)
            elif self.value_type == "bool":
                str(value).lower() in ('true', 'false', '1', '0', 'yes', 'no')
            return True
        except:
            return False

class FastFlagDatabase:
    def __init__(self):
        self.flags: Dict[str, FastFlag] = {}
        self.load_database()
        
    def load_database(self):
        try:
            with open('data/fastflags.json', 'r') as f:
                data = json.load(f)
                for flag_data in data:
                    flag = FastFlag(**flag_data)
                    self.flags[flag.name] = flag
        except FileNotFoundError:
            self.create_default_database()
            
    def create_default_database(self):
        default_flags = [
            FastFlag(
                name="DFIntTaskSchedulerTargetFps",
                description="Controls target FPS for the game",
                default_value=60,
                value_type="int",
                category="Performance",
                exploitable=True,
                exploit_description="Can be used to unlock FPS"
            ),
            FastFlag(
                name="FFlagDisableGPUAcceleration",
                description="Controls GPU acceleration for rendering",
                default_value=False,
                value_type="bool",
                category="Graphics",
                exploitable=True,
                exploit_description="Can improve performance on some systems"
            ),
            FastFlag(
                name="DFIntConnectionThrottleMaxExponent",
                description="Controls network throttling",
                default_value=16,
                value_type="int",
                category="Network",
                exploitable=True,
                exploit_description="Can reduce network throttling"
            ),
            FastFlag(
                name="DFStringCrashUploadToBacktraceBaseUrl",
                description="Crash reporting URL",
                default_value="",
                value_type="string",
                category="Debug",
                exploitable=False
            ),
            FastFlag(
                name="FFlagDebugGraphicsPrefer",
                description="Graphics preference mode",
                default_value="Integrated",
                value_type="string",
                category="Graphics",
                exploitable=True,
                exploit_description="Can force discrete GPU usage"
            )
        ]
        
        for flag in default_flags:
            self.flags[flag.name] = flag
            
    def get_all_flags(self) -> List[FastFlag]:
        return list(self.flags.values())
        
    def get_flag(self, name: str) -> Optional[FastFlag]:
        return self.flags.get(name)
        
    def search_flags(self, query: str) -> List[FastFlag]:
        query = query.lower()
        return [
            flag for flag in self.flags.values()
            if query in flag.name.lower() or query in flag.description.lower()
        ] 
    
    def import_flags(self, data: list):
        """Import flags from a JSON-compatible dictionary list"""
        for flag_data in data:
            try:
                # Validate required fields
                required_fields = {'name', 'description', 'default_value', 'value_type', 'category'}
                if not all(field in flag_data for field in required_fields):
                    raise ValueError(f"Missing required fields in flag: {flag_data.get('name', 'unknown')}")
                
                # Create FastFlag object
                flag = FastFlag(**flag_data)
                self.flags[flag.name] = flag
                
            except Exception as e:
                print(f"Error importing flag: {str(e)}")
                continue
                
        self.save_database()
    
    def export_flags(self) -> list:
        """Export flags as a JSON-compatible dictionary list"""
        return [asdict(flag) for flag in self.flags.values()]
    
    def save_database(self):
        """Save the current database to disk"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/fastflags.json', 'w') as f:
                json.dump(self.export_flags(), f, indent=4)
        except Exception as e:
            print(f"Error saving database: {str(e)}")
    
    def get_flags_by_category(self, category: str) -> List[FastFlag]:
        """Get all flags in a specific category"""
        return [flag for flag in self.flags.values() if flag.category == category]
        
    def get_exploitable_flags(self) -> List[FastFlag]:
        """Get all flags marked as exploitable"""
        return [flag for flag in self.flags.values() if flag.exploitable]
        
    def get_flags_for_game(self, game_name: str) -> List[FastFlag]:
        """Get flags recommended for a specific game"""
        return [
            flag for flag in self.flags.values()
            if hasattr(flag, 'recommended_games') and
            (game_name in flag.recommended_games or 'All' in flag.recommended_games or
             self._matches_game_category(game_name, flag.recommended_games))
        ]
        
    def _matches_game_category(self, game_name: str, recommended_games: List[str]) -> bool:
        """Check if game matches a category in recommended games"""
        game_categories = {
            "FPS Games": ["Arsenal", "Phantom Forces", "Bad Business"],
            "RPG Games": ["Adopt Me", "Blox Fruits", "Pet Simulator"],
            "Fighting Games": ["Blox Fruits", "Your Bizarre Adventure", "ABA"]
        }
        
        for category in recommended_games:
            if category in game_categories and game_name in game_categories[category]:
                return True
        return False