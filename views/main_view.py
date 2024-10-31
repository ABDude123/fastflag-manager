from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLineEdit, QListWidget, QLabel, QCheckBox,
                           QPushButton, QTextEdit, QDialog, QMessageBox,
                           QComboBox, QTabWidget, QListWidgetItem, QBrush, QColor)
from PyQt6.QtCore import Qt
import json
from models.config_manager import ConfigManager
from resources import Icons

class JsonImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Custom FastFlags")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # JSON input area
        self.json_input = QTextEdit()
        self.json_input.setPlaceholderText(
            '[\n  {\n    "name": "DFFlag...",\n    "description": "...",\n    '
            '"default_value": "...",\n    "value_type": "...",\n    '
            '"category": "..."\n  }\n]'
        )
        layout.addWidget(self.json_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.cancel_button = QPushButton("Cancel")
        
        self.import_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_json_data(self):
        try:
            return json.loads(self.json_input.toPlainText())
        except json.JSONDecodeError:
            return None

class MainView(QWidget):
    def __init__(self, database, favorites):
        super().__init__()
        self.database = database
        self.favorites = favorites
        self.config = ConfigManager()
        self.icons = Icons.load()
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        
        # Left panel
        left_panel = QVBoxLayout()
        
        # Search and filter
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search FastFlags...")
        self.search_bar.textChanged.connect(self.update_list)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "Performance", "Graphics", "Network", "Debug"])
        self.category_filter.currentTextChanged.connect(self.update_list)
        
        self.game_filter = QComboBox()
        self.game_filter.addItems([
            "All Games",
            "Arsenal",
            "Phantom Forces",
            "Adopt Me",
            "Blox Fruits",
            "Prison Life",
            "Jailbreak",
            "FPS Games",
            "RPG Games",
            "Fighting Games"
        ])
        self.game_filter.currentTextChanged.connect(self.update_list)
        
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.category_filter)
        search_layout.addWidget(self.game_filter)
        left_panel.addLayout(search_layout)
        
        # Tabs for All/Favorites/Exploitable
        self.tabs = QTabWidget()
        
        # All flags list
        self.flags_list = QListWidget()
        self.flags_list.itemClicked.connect(self.show_flag_details)
        self.tabs.addTab(self.flags_list, "All Flags")
        
        # Favorites list
        self.favorites_list = QListWidget()
        self.favorites_list.itemClicked.connect(self.show_flag_details)
        self.tabs.addTab(self.favorites_list, "Favorites")
        
        # Exploitable flags list
        self.exploitable_list = QListWidget()
        self.exploitable_list.itemClicked.connect(self.show_flag_details)
        self.tabs.addTab(self.exploitable_list, "Exploitable")
        
        self.tabs.currentChanged.connect(self.update_list)
        left_panel.addWidget(self.tabs)
        
        # Right panel (details)
        right_panel = QVBoxLayout()
        
        # Details panel
        self.details_panel = QWidget()
        details_layout = QVBoxLayout()
        
        # Flag name and category
        name_layout = QHBoxLayout()
        self.flag_name = QLabel()
        self.flag_category = QLabel()
        name_layout.addWidget(self.flag_name)
        name_layout.addWidget(self.flag_category)
        details_layout.addLayout(name_layout)
        
        # Description
        self.flag_description = QLabel()
        self.flag_description.setWordWrap(True)
        details_layout.addWidget(self.flag_description)
        
        # Exploit info (if applicable)
        self.exploit_info = QLabel()
        self.exploit_info.setStyleSheet("color: red;")
        self.exploit_info.setWordWrap(True)
        details_layout.addWidget(self.exploit_info)
        
        # Value controls
        value_layout = QHBoxLayout()
        self.flag_value = QLineEdit()
        self.flag_value.textChanged.connect(self.value_changed)
        self.flag_toggle = QCheckBox("Enable")
        self.flag_toggle.stateChanged.connect(self.toggle_changed)
        
        value_layout.addWidget(QLabel("Value:"))
        value_layout.addWidget(self.flag_value)
        value_layout.addWidget(self.flag_toggle)
        details_layout.addLayout(value_layout)
        
        # Favorite button
        self.favorite_button = QPushButton("Add to Favorites")
        self.favorite_button.clicked.connect(self.toggle_favorite)
        details_layout.addWidget(self.favorite_button)
        
        # Apply button
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self.apply_changes)
        details_layout.addWidget(self.apply_button)
        
        self.details_panel.setLayout(details_layout)
        right_panel.addWidget(self.details_panel)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, stretch=1)
        main_layout.addLayout(right_panel, stretch=1)
        
        self.setLayout(main_layout)
        self.current_flag = None
        
        self.update_list()
        
        # Add icons to elements
        self.search_bar.addAction(self.icons["search"], QLineEdit.ActionPosition.LeadingPosition)
        self.favorite_button.setIcon(self.icons["unfavorite"])
        self.apply_button.setIcon(self.icons["apply"])
        
        # Add tooltips
        self.search_bar.setToolTip("Search for FastFlags by name, description, or category")
        self.category_filter.setToolTip("Filter FastFlags by category")
        self.flag_value.setToolTip("Enter the value for this FastFlag")
        self.flag_toggle.setToolTip("Enable or disable this FastFlag")
        
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
            
            QLineEdit:focus {
                border-color: #007AFF;
            }
            
            QPushButton {
                background: #007AFF;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            
            QPushButton:hover {
                background: #0051FF;
            }
            
            QPushButton:pressed {
                background: #003ECB;
            }
            
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            
            QListWidget::item:selected {
                background: #E5F1FB;
                color: #007AFF;
            }
            
            QLabel {
                color: #333;
            }
            
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            
            QTabBar::tab {
                background: #f5f5f5;
                padding: 8px 16px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background: white;
                border-bottom: none;
            }
            
            .exploit-info {
                color: #FF3B30;
                font-weight: bold;
            }
        """)
    
    def update_list(self):
        current_tab = self.tabs.currentWidget()
        search_text = self.search_bar.text().lower()
        category = self.category_filter.currentText()
        game = self.game_filter.currentText()
        
        # Clear all lists
        self.flags_list.clear()
        self.favorites_list.clear()
        self.exploitable_list.clear()
        
        # Get filtered flags
        flags = self.database.get_flags_for_game(game) if game != "All Games" else self.database.get_all_flags()
        
        if category != "All Categories":
            flags = [f for f in flags if f.category == category]
            
        if search_text:
            flags = [f for f in flags 
                    if search_text in f.name.lower() or 
                       search_text in f.description.lower()]
        
        # Update appropriate list based on current tab
        current_list = None
        if current_tab == self.flags_list:
            current_list = self.flags_list
            flags_to_show = flags
        elif current_tab == self.favorites_list:
            current_list = self.favorites_list
            flags_to_show = [f for f in flags if self.favorites.is_favorite(f)]
        else:  # exploitable list
            current_list = self.exploitable_list
            flags_to_show = [f for f in flags if f.exploitable]
            
        for flag in flags_to_show:
            item = QListWidgetItem()
            item.setText(flag.name)
            
            # Add appropriate icon
            if flag.exploitable:
                item.setIcon(self.icons["exploit"])
            elif flag.category in self.icons:
                item.setIcon(self.icons[flag.category.lower()])
                
            # Add tooltip with description
            item.setToolTip(f"{flag.description}\nCategory: {flag.category}")
            
            # Highlight matching text if searching
            if search_text:
                if search_text in flag.name.lower():
                    item.setForeground(QBrush(QColor("#007AFF")))
                    
            current_list.addItem(item)
    
    def toggle_favorite(self):
        if self.current_flag:
            if self.favorites.is_favorite(self.current_flag):
                self.favorites.remove_favorite(self.current_flag)
                self.favorite_button.setText("Add to Favorites")
            else:
                self.favorites.add_favorite(self.current_flag)
                self.favorite_button.setText("Remove from Favorites")
            self.update_list()
    
    def show_flag_details(self, item):
        flag = self.database.get_flag(item.text())
        if flag:
            self.current_flag = flag
            self.flag_name.setText(flag.name)
            self.flag_description.setText(flag.description)
            
            # Show current value if flag is active
            current_value = self.config.get_flag_value(flag.name)
            if current_value is not None:
                self.flag_value.setText(str(current_value))
                self.flag_toggle.setChecked(True)
            else:
                self.flag_value.setText(str(flag.default_value))
                self.flag_toggle.setChecked(False)
                
            self.favorite_checkbox.setChecked(self.favorites.is_favorite(flag))
            
            # Enable/disable value input based on toggle
            self.flag_value.setEnabled(self.flag_toggle.isChecked())
            
    def value_changed(self, text):
        if self.current_flag and self.flag_toggle.isChecked():
            try:
                # Convert value to appropriate type
                if self.current_flag.value_type == "int":
                    value = int(text)
                elif self.current_flag.value_type == "float":
                    value = float(text)
                elif self.current_flag.value_type == "bool":
                    value = text.lower() in ('true', '1', 'yes')
                else:
                    value = text
                    
                self.config.set_flag_value(self.current_flag.name, value)
            except ValueError:
                pass  # Invalid value, ignore
                
    def toggle_changed(self, state):
        if self.current_flag:
            self.flag_value.setEnabled(state)
            if state:
                self.value_changed(self.flag_value.text())
            else:
                self.config.remove_flag(self.current_flag.name)
                
    def apply_changes(self):
        if self.current_flag:
            success, message = self.config.set_flag_value(
                self.current_flag.name,
                self.flag_value.text()
            )
            
            if success:
                QMessageBox.information(
                    self,
                    "Success",
                    f"FastFlag applied successfully!\n{message}\n\n"
                    "Please restart Roblox for changes to take effect."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Warning",
                    f"FastFlag may not be working: {message}"
                )
    
    def show_custom_import(self):
        dialog = JsonImportDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            json_data = dialog.get_json_data()
            if json_data:
                try:
                    self.database.import_flags(json_data)
                    self.update_list()
                    QMessageBox.information(
                        self,
                        "Success",
                        "Custom FastFlags imported successfully!"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to import FastFlags: {str(e)}"
                    )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Invalid JSON format"
                )