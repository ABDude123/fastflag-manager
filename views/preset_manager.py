class PresetManager(QWidget):
    def __init__(self, database, config):
        super().__init__()
        self.database = database
        self.config = config
        
        self.presets = {
            "Ultimate FPS Boost": {
                "DFIntTaskSchedulerTargetFps": 0,
                "FFlagDisableSpeculativeGPUMemoryAllocation": True,
                "DFIntGPUTextureReductionPercentage": 75,
                "FFlagDisablePostFx": True
            },
            "PvP Advantage": {
                "DFIntNetworkResponseWindow": 50,
                "DFIntPlayerNetworkStates": 240,
                "DFIntHitboxExpansionSize": 2,
                "FFlagDisableAnimationStateReplication": True
            },
            "Stealth Mode": {
                "FFlagDisableAssetLoading": True,
                "DFIntRenderDistance": 5000,
                "FFlagBypassTerrainChecks": True
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        for preset_name, flags in self.presets.items():
            btn = QPushButton(preset_name)
            btn.clicked.connect(lambda checked, n=preset_name: self.apply_preset(n))
            layout.addWidget(btn)
            
        self.setLayout(layout)
        
    def apply_preset(self, preset_name):
        flags = self.presets[preset_name]
        for flag_name, value in flags.items():
            self.config.set_flag_value(flag_name, value) 