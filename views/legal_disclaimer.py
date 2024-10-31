from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QScrollArea, QWidget
from PyQt6.QtCore import Qt

class LegalDisclaimerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Terms of Use")
        self.setMinimumSize(600, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create scrollable area for disclaimer text
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        
        disclaimer_text = [
            "<h2>Educational Purpose Statement</h2>",
            
            "<p>This software is designed for <b>educational and research purposes only</b>. "
            "It serves as a tool for understanding game development, network protocols, "
            "and system optimization techniques.</p>",
            
            "<h3>Usage Guidelines:</h3>",
            "<ul>"
            "<li>This tool is intended for educational research and testing</li>"
            "<li>Users are responsible for compliance with all applicable terms of service</li>"
            "<li>This software does not modify any game files</li>"
            "<li>All features are based on publicly available documentation</li>"
            "</ul>",
            
            "<h3>Technical Information:</h3>",
            "<p>This application provides access to FastFlags, which are standard "
            "configuration options used in game development for testing and optimization. "
            "These settings are commonly used by developers and technical users.</p>",
            
            "<h3>User Responsibility:</h3>",
            "<p>Users are solely responsible for:</p>"
            "<ul>"
            "<li>How they use this educational tool</li>"
            "<li>Ensuring compliance with game terms of service</li>"
            "<li>Understanding the impact of configuration changes</li>"
            "</ul>",
            
            "<h3>Disclaimer:</h3>",
            "<p>This software:</p>"
            "<ul>"
            "<li>Is provided 'as-is' without any warranties</li>"
            "<li>Is for educational purposes only</li>"
            "<li>Should be used responsibly and ethically</li>"
            "<li>May not be suitable for all users or purposes</li>"
            "</ul>",
            
            "<p>By using this software, you acknowledge that you have read and understood "
            "these terms and agree to use this educational tool responsibly.</p>"
        ]
        
        for text in disclaimer_text:
            label = QLabel(text)
            label.setWordWrap(True)
            label.setTextFormat(Qt.TextFormat.RichText)
            scroll_layout.addWidget(label)
            
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Agreement checkbox
        self.agree_checkbox = QCheckBox("I understand and agree to use this educational tool responsibly")
        layout.addWidget(self.agree_checkbox)
        
        # Buttons
        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(self.accept)
        self.accept_button.setEnabled(False)
        self.agree_checkbox.stateChanged.connect(
            lambda state: self.accept_button.setEnabled(state == Qt.CheckState.Checked)
        )
        
        self.reject_button = QPushButton("Decline")
        self.reject_button.clicked.connect(self.reject)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.reject_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout) 