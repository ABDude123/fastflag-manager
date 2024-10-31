class TestEnvironment(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def test_flag(self, flag_name, value):
        # Backup current settings
        original_value = self.config.get_flag_value(flag_name)
        
        # Apply test value
        self.config.set_flag_value(flag_name, value)
        
        # Monitor for 30 seconds
        results = self.monitor_performance(30)
        
        # Restore original
        self.config.set_flag_value(flag_name, original_value)
        
        return results 