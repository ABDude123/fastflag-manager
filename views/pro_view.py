from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTextEdit, QLabel, QLineEdit, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt
import openai
import json
from pathlib import Path
import os
import subprocess
from .lua_executor import LuaExecutorWidget

class AIFlagGeneratorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Initialize OpenAI (you'll need to set your API key)
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Description input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Describe what you want to achieve (e.g., 'Generate flags to improve PvP performance')"
        )
        layout.addWidget(QLabel("Describe your goal:"))
        layout.addWidget(self.description_input)
        
        # Generate button
        self.generate_btn = QPushButton("Generate FastFlags")
        self.generate_btn.clicked.connect(self.generate_flags)
        layout.addWidget(self.generate_btn)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(QLabel("Generated FastFlags:"))
        layout.addWidget(self.results_display)
        
        # Import button
        self.import_btn = QPushButton("Import Generated Flags")
        self.import_btn.clicked.connect(self.import_flags)
        layout.addWidget(self.import_btn)
        
        self.setLayout(layout)
        
    def generate_flags(self):
        try:
            prompt = self.description_input.toPlainText()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Roblox FastFlag expert. Generate FastFlags in JSON format that achieve the user's goal."},
                    {"role": "user", "content": f"Generate FastFlags for: {prompt}"}
                ]
            )
            
            self.results_display.setText(response.choices[0].message.content)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate flags: {str(e)}")
            
    def import_flags(self):
        try:
            json_text = self.results_display.toPlainText()
            flags = json.loads(json_text)
            self.parent().database.import_flags(flags)
            QMessageBox.information(self, "Success", "Generated flags imported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import flags: {str(e)}")

class ProView(QWidget):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Pro features unlock
        self.unlock_widget = QWidget()
        unlock_layout = QHBoxLayout()
        self.unlock_code = QLineEdit()
        self.unlock_code.setPlaceholderText("Enter unlock code")
        self.unlock_btn = QPushButton("Unlock Pro Features")
        self.unlock_btn.clicked.connect(self.check_unlock_code)
        
        unlock_layout.addWidget(self.unlock_code)
        unlock_layout.addWidget(self.unlock_btn)
        self.unlock_widget.setLayout(unlock_layout)
        layout.addWidget(self.unlock_widget)
        
        # Pro features (initially hidden)
        self.pro_features = QTabWidget()
        self.pro_features.setVisible(False)
        
        # AI Generator tab
        self.ai_generator = AIFlagGeneratorWidget(self)
        self.pro_features.addTab(self.ai_generator, "AI Flag Generator")
        
        # Lua Executor tab
        self.lua_executor = LuaExecutorWidget()
        self.pro_features.addTab(self.lua_executor, "Lua Executor")
        
        layout.addWidget(self.pro_features)
        self.setLayout(layout)
        
    def check_unlock_code(self):
        if self.unlock_code.text().lower() == "lifehacks":
            self.unlock_widget.setVisible(False)
            self.pro_features.setVisible(True)
            QMessageBox.information(self, "Success", "Pro features unlocked!")
        else:
            QMessageBox.warning(self, "Invalid Code", "Incorrect unlock code") 