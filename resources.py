from PyQt6.QtGui import QIcon
from pathlib import Path

RESOURCE_PATH = Path(__file__).parent / "resources"

class Icons:
    @staticmethod
    def load():
        return {
            "app": QIcon(str(RESOURCE_PATH / "app.png")),
            "search": QIcon(str(RESOURCE_PATH / "search.png")),
            "favorite": QIcon(str(RESOURCE_PATH / "favorite.png")),
            "unfavorite": QIcon(str(RESOURCE_PATH / "unfavorite.png")),
            "exploit": QIcon(str(RESOURCE_PATH / "exploit.png")),
            "performance": QIcon(str(RESOURCE_PATH / "performance.png")),
            "graphics": QIcon(str(RESOURCE_PATH / "graphics.png")),
            "network": QIcon(str(RESOURCE_PATH / "network.png")),
            "debug": QIcon(str(RESOURCE_PATH / "debug.png")),
            "apply": QIcon(str(RESOURCE_PATH / "apply.png")),
            "import": QIcon(str(RESOURCE_PATH / "import.png")),
            "export": QIcon(str(RESOURCE_PATH / "export.png")),
            "pro": QIcon(str(RESOURCE_PATH / "pro.png")),
            "lock": QIcon(str(RESOURCE_PATH / "lock.png")),
        } 