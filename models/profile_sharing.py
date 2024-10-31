from datetime import datetime

class ProfileSharing:
    def __init__(self):
        self.api_url = "https://api.example.com/profiles"
        
    def share_profile(self, profile_name, flags):
        profile_data = {
            "name": profile_name,
            "flags": flags,
            "created_by": self.get_user(),
            "timestamp": datetime.now().isoformat()
        }
        return self.upload_profile(profile_data)
        
    def get_shared_profiles(self):
        return self.fetch_profiles() 