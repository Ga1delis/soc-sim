from dataclasses import dataclass
from typing import Set

@dataclass
class Location:
    name: str

    open_hour: int = 0
    close_hour: int = 24
    open_days: Set[int] = None
    wealth_threshold: float = 0.0
    energy_change: int = 0
    hunger_change: int = 0
    social_change: int = 0
    
    def __post_init__(self):
        if self.open_days is None:
            self.open_days = {0, 1, 2, 3, 4, 5, 6}
    
    def is_open(self, hour_of_day: int, day_of_week: int) -> bool:
        if day_of_week not in self.open_days:
            return False
        
        if self.close_hour > self.open_hour:
            return self.open_hour <= hour_of_day < self.close_hour
        else:
            return hour_of_day >= self.open_hour or hour_of_day < self.close_hour
