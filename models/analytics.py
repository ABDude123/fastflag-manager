from collections import Counter

class FlagAnalytics:
    def __init__(self):
        self.stats = {}
        
    def track_flag_usage(self, flag_name, value):
        if flag_name not in self.stats:
            self.stats[flag_name] = {
                "uses": 0,
                "popular_values": Counter(),
                "success_rate": 0
            }
        
        self.stats[flag_name]["uses"] += 1
        self.stats[flag_name]["popular_values"][str(value)] += 1 