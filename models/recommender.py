class SmartRecommender:
    def __init__(self, database, analytics):
        self.database = database
        self.analytics = analytics
        
    def get_recommendations(self, current_flags):
        recommendations = []
        
        # Analyze current setup
        performance_score = self.calculate_performance_score(current_flags)
        
        # Find complementary flags
        for flag in self.database.get_all_flags():
            if self.would_improve_setup(flag, current_flags, performance_score):
                recommendations.append((flag, self.calculate_impact_score(flag)))
                
        return sorted(recommendations, key=lambda x: x[1], reverse=True) 