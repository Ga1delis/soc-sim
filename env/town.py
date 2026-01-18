from typing import Dict, List, Optional
from env.location import Location

class Town:
    def __init__(self):
        self.hour_abs = 0
        self.location_registry: Dict[str, Location] = self._create_locations()
        self.locations: Dict[str, List[object]] = {
            name: [] for name in self.location_registry.keys()
        }
    
    def _create_locations(self) -> Dict[str, Location]:
        locations = {}
        locations["home"] = Location(
            name="home",
            open_hour=0,
            close_hour=24,
            energy_change=12,
            social_change=-1,
        )
        locations["work"] = Location(
            name="work",
            open_hour=9,
            close_hour=17,
            open_days={0, 1, 2, 3, 4},
            energy_change=-8,
            hunger_change=2,
        )

        locations["shop"] = Location(
            name="shop",
            open_hour=8,
            close_hour=20,
            open_days={0, 1, 2, 3, 4, 5},
            energy_change=-4,
        )
        
        locations["cafe"] = Location(
            name="cafe",
            open_hour=7,
            close_hour=21,
            open_days={0, 1, 2, 3, 4, 5, 6},
            energy_change=-2,
        )

        locations["park"] = Location(
            name="park",
            open_hour=6,
            close_hour=22,
            open_days={0, 1, 2, 3, 4, 5, 6},
            energy_change=2,
        )

        locations["gym"] = Location(
            name="gym",
            open_hour=6,
            close_hour=22,
            open_days={0, 1, 2, 3, 4, 5, 6},
            wealth_threshold=0.4,
            energy_change=-15,
            hunger_change=3,
        )
    
        locations["library"] = Location(
            name="library",
            open_hour=9,
            close_hour=18,
            open_days={0, 1, 2, 3, 4, 5},
            energy_change=1,
        )
        
        locations["restaurant"] = Location(
            name="restaurant",
            open_hour=11,
            close_hour=22,
            open_days={0, 1, 2, 3, 4, 5, 6},
            wealth_threshold=0.6,
            energy_change=-3,
            hunger_change=-50,
        )
        
        locations["bar"] = Location(
            name="bar",
            open_hour=17,
            close_hour=2,
            open_days={0, 1, 2, 3, 4, 5, 6},
            wealth_threshold=0.4,
            energy_change=-5,
        )
        
        locations["hospital"] = Location(
            name="hospital",
            open_hour=0,
            close_hour=24,
            open_days={0, 1, 2, 3, 4, 5, 6},
            energy_change=-3,
        )
        
        return locations

    @property
    def hour_of_day(self) -> int:
        return self.hour_abs % 24

    @property
    def day_index(self) -> int:
        return self.hour_abs // 24

    @property
    def day_of_week(self) -> int:
        return self.day_index % 7

    def is_night(self) -> bool:
        h = self.hour_of_day
        return h >= 22 or h < 6
    
    def is_weekend(self) -> bool:
        return self.day_of_week >= 5
    
    def get_location(self, location_name: str) -> Optional[Location]:
        return self.location_registry.get(location_name)
    
    def is_location_open(self, location_name: str) -> bool:
        loc = self.get_location(location_name)
        if not loc:
            return False
        return loc.is_open(self.hour_of_day, self.day_of_week)
    
    def can_enter_location(self, location_name: str, agent=None) -> bool:
        if not self.is_location_open(location_name):
            return False        
        loc = self.get_location(location_name)
        if not loc:
            return False
        if agent and agent.wealth < loc.wealth_threshold:
            return False
            
        return True
 
    def get_occupancy(self, location_name: str) -> int:
        return len(self.locations.get(location_name, []))

    def add_agent(self, agent, location: str = "home"):
        if location not in self.location_registry:
            raise ValueError(f"Unknown location: {location}")
        agent.location = location
        self.locations[location].append(agent)

    def move_agent(self, agent, new_location: str):
        if new_location not in self.location_registry:
            raise ValueError(f"Unknown location: {new_location}")
        old = agent.location
        if old == new_location:
            return
        if old in self.locations and agent in self.locations[old]:
            self.locations[old].remove(agent)
        self.locations[new_location].append(agent)
        agent.location = new_location

    def step_time(self):
        self.hour_abs += 1
