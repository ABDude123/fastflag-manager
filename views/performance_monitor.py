class PerformanceMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.start_monitoring()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.fps_label = QLabel("FPS: --")
        self.memory_label = QLabel("Memory: --")
        self.ping_label = QLabel("Ping: --")
        layout.addWidget(self.fps_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.ping_label)
        self.setLayout(layout)
        
    def start_monitoring(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every second
        
    def update_stats(self):
        # Get stats from Roblox process
        process = self.get_roblox_process()
        if process:
            self.fps_label.setText(f"FPS: {self.get_fps()}")
            self.memory_label.setText(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
            self.ping_label.setText(f"Ping: {self.get_ping()}ms") 