import json
from typing import List, Set
from models.fastflag_database import FastFlag

class FavoritesManager:
    def __init__(self):
        self.favorites: Set[str] = set()
        self.load_favorites()
        
    def load_favorites(self):
        try:
            with open('data/favorites.json', 'r') as f:
                self.favorites = set(json.load(f))
        except FileNotFoundError:
            self.favorites = set()
            
    def save_favorites(self):
        with open('data/favorites.json', 'w') as f:
            json.dump(list(self.favorites), f)
            
    def add_favorite(self, flag: FastFlag):
        self.favorites.add(flag.name)
        self.save_favorites()
        
    def remove_favorite(self, flag: FastFlag):
        self.favorites.discard(flag.name)
        self.save_favorites()
        
    def is_favorite(self, flag: FastFlag) -> bool:
        return flag.name in self.favorites
        
    def get_favorites(self) -> List[str]:
        return list(self.favorites) 