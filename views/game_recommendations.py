from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel

class GameRecommendationsDialog(QDialog):
    def __init__(self, database, game_name: str, parent=None):
        super().__init__(parent)
        self.database = database
        self.game_name = game_name
        self.setWindowTitle(f"Recommended Flags for {game_name}")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Description
        description = QLabel(f"Recommended FastFlags for {self.game_name}:")
        layout.addWidget(description)
        
        # Flags list
        self.flags_list = QListWidget()
        recommended_flags = self.database.get_flags_for_game(self.game_name)
        
        for flag in recommended_flags:
            self.flags_list.addItem(
                f"{flag.name}: {flag.description}\n"
                f"Recommended value: {flag.default_value}\n"
                f"Effect: {flag.exploit_description}"
            )
            
        layout.addWidget(self.flags_list)
        
        # Apply all button
        apply_all = QPushButton("Apply All Recommended Flags")
        apply_all.clicked.connect(self.apply_all_flags)
        layout.addWidget(apply_all)
        
        self.setLayout(layout)
        
    def apply_all_flags(self):
        flags = self.database.get_flags_for_game(self.game_name)
        for flag in flags:
            self.parent().config.set_flag_value(flag.name, flag.default_value) 