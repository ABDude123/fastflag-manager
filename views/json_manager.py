from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTextEdit, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import json
from pathlib import Path

class JsonManagerDialog(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("FastFlag JSON Manager")
        self.setMinimumSize(800, 600)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            "Import/Export FastFlags in JSON format. You can edit the JSON directly "
            "or load/save from/to files."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # JSON Editor
        self.json_editor = QTextEdit()
        self.json_editor.setPlaceholderText("Paste or edit JSON here...")
        layout.addWidget(self.json_editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.load_file_btn = QPushButton("Load from File")
        self.save_file_btn = QPushButton("Save to File")
        self.import_btn = QPushButton("Import to Database")
        self.export_btn = QPushButton("Export from Database")
        
        self.load_file_btn.clicked.connect(self.load_from_file)
        self.save_file_btn.clicked.connect(self.save_to_file)
        self.import_btn.clicked.connect(self.import_to_database)
        self.export_btn.clicked.connect(self.export_from_database)
        
        button_layout.addWidget(self.load_file_btn)
        button_layout.addWidget(self.save_file_btn)
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.export_btn)
        
        layout.addLayout(button_layout)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load FastFlags JSON",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.json_editor.setText(json.dumps(data, indent=4))
                QMessageBox.information(
                    self,
                    "Success",
                    "JSON file loaded successfully!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to load JSON file: {str(e)}"
                )
                
    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save FastFlags JSON",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                json_text = self.json_editor.toPlainText()
                # Validate JSON before saving
                json.loads(json_text)
                
                with open(file_path, 'w') as f:
                    f.write(json_text)
                QMessageBox.information(
                    self,
                    "Success",
                    "JSON file saved successfully!"
                )
            except json.JSONDecodeError:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Invalid JSON format"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save JSON file: {str(e)}"
                )
                
    def import_to_database(self):
        try:
            json_text = self.json_editor.toPlainText()
            data = json.loads(json_text)
            
            self.database.import_flags(data)
            QMessageBox.information(
                self,
                "Success",
                "FastFlags imported to database successfully!"
            )
            self.accept()
        except json.JSONDecodeError:
            QMessageBox.critical(
                self,
                "Error",
                "Invalid JSON format"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to import FastFlags: {str(e)}"
            )
            
    def export_from_database(self):
        try:
            data = self.database.export_flags()
            self.json_editor.setText(json.dumps(data, indent=4))
            QMessageBox.information(
                self,
                "Success",
                "FastFlags exported from database successfully!"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export FastFlags: {str(e)}"
            ) 