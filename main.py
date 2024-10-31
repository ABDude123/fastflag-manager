import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog, QMessageBox, QDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
import rumps  # For menu bar integration
import json
from pathlib import Path
import os

from views.main_view import MainView
from views.pro_view import ProView
from models.fastflag_database import FastFlagDatabase
from models.favorites_manager import FavoritesManager
from views.json_manager import JsonManagerDialog
from views.legal_disclaimer import LegalDisclaimerDialog
from utils.updater import AutoUpdater

class FastFlagManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastFlag Manager")
        self.setMinimumSize(800, 600)
        
        # Check if user has accepted disclaimer
        if not self.check_disclaimer_accepted():
            self.show_disclaimer()
            
        # Initialize managers
        self.database = FastFlagDatabase()
        self.favorites = FavoritesManager()
        
        # Setup UI stack
        self.stack = QStackedWidget()
        self.main_view = MainView(self.database, self.favorites)
        self.pro_view = ProView(self.database)
        
        self.stack.addWidget(self.main_view)
        self.stack.addWidget(self.pro_view)
        self.setCentralWidget(self.stack)
        
        self.setup_menubar()
        self.setup_statusbar()
        self.setup_system_tray()
        
        self.updater = AutoUpdater()
        self.check_for_updates()
        
    def setup_menubar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        json_manager_action = QAction("JSON Manager", self)
        json_manager_action.triggered.connect(self.show_json_manager)
        file_menu.addAction(json_manager_action)
        
        import_action = QAction("Quick Import", self)
        import_action.triggered.connect(self.import_fastflags)
        file_menu.addAction(import_action)
        
        export_action = QAction("Quick Export", self)
        export_action.triggered.connect(self.export_fastflags)
        file_menu.addAction(export_action)
        
    def setup_system_tray(self):
        self.tray_app = rumps.App("FastFlag Manager", quit_button=None)
        self.update_tray_menu()
        
    def update_tray_menu(self):
        # Update tray menu with favorite fastflags
        menu_items = []
        for flag in self.favorites.get_favorites():
            menu_items.append(rumps.MenuItem(flag.name, callback=self.toggle_flag))
        self.tray_app.menu.clear()
        self.tray_app.menu = menu_items
        
    def toggle_flag(self, sender):
        # Toggle the selected flag
        pass
        
    def import_fastflags(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import FastFlags",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.database.import_flags(data)
                    self.main_view.update_list()
                    QMessageBox.information(
                        self,
                        "Success",
                        "FastFlags imported successfully!"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to import FastFlags: {str(e)}"
                )
                
    def export_fastflags(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export FastFlags",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                flags_data = self.database.export_flags()
                with open(file_path, 'w') as f:
                    json.dump(flags_data, f, indent=4)
                QMessageBox.information(
                    self,
                    "Success",
                    "FastFlags exported successfully!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to export FastFlags: {str(e)}"
                )
        
    def show_json_manager(self):
        dialog = JsonManagerDialog(self.database, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.main_view.update_list()
        
    def check_disclaimer_accepted(self) -> bool:
        try:
            config_path = Path('data/config.json')
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('disclaimer_accepted', False)
            return False
        except:
            return False
            
    def save_disclaimer_accepted(self):
        try:
            config_path = Path('data/config.json')
            config = {}
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
            config['disclaimer_accepted'] = True
            
            os.makedirs('data', exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f)
        except:
            pass
            
    def show_disclaimer(self):
        dialog = LegalDisclaimerDialog(self)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            self.save_disclaimer_accepted()
        else:
            sys.exit()
        
    async def check_for_updates(self):
        """Check for and handle updates"""
        has_update, download_url = await self.updater.check_for_updates()
        
        if has_update:
            reply = QMessageBox.question(
                self,
                "Update Available",
                "A new version is available. Would you like to update now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.statusBar().showMessage("Downloading update...")
                dmg_path = await self.updater.download_update(download_url)
                
                if dmg_path:
                    self.statusBar().showMessage("Installing update...")
                    if self.updater.install_update(dmg_path):
                        QMessageBox.information(
                            self,
                            "Update Complete",
                            "The update has been installed. Please restart the application."
                        )
                        sys.exit(0)
                    else:
                        QMessageBox.critical(
                            self,
                            "Update Failed",
                            "Failed to install the update."
                        )

def main():
    app = QApplication(sys.argv)
    window = FastFlagManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 