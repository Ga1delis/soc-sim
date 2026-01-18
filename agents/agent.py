import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class Persona:
    name: str
    age: int
    job: str
    description: str

@dataclass
class AgentProfile:
    persona: Persona

    work_start: int = 9
    work_end: int = 17
    weekend_worker: bool = False
    hunger_gain: int = 6
    energy_loss: int = 2
    social_loss: int = 3
    stress_gain: int = 2
    entertainment_loss: int = 2
    health_loss: int = 1
    hunger_eat: int = 70
    hunger_shop: int = 85
    energy_sleep: int = 25
    social_seek: int = 55
    stress_seek_relief: int = 60
    entertainment_seek: int = 40
    health_seek_care: int = 50
    sociability: float = 0.5
    wealth_level: float = 0.5
    talk_at_work: bool = False

class Agent:
    def __init__(self, profile: AgentProfile, memory_store=None, llm=None):
        self.p = profile
        self.memory = memory_store
        self.llm = llm
        self.energy = random.randint(60, 95)
        self.hunger = random.randint(10, 40)
        self.social = random.randint(40, 90)
      
        self.health = random.randint(70, 100)
        self.stress = random.randint(10, 40)
        self.entertainment = random.randint(40, 80)
        self.comfort = random.randint(50, 90)

        self.food_at_home = random.randint(1, 5)
        self.wealth = profile.wealth_level

        self.location = "home"
        self.busy_until_abs_hour = 0

    def clamp(self):
        self.energy = max(0, min(100, self.energy))
        self.hunger = max(0, min(100, self.hunger))
        self.social = max(0, min(100, self.social))
        self.health = max(0, min(100, self.health))
        self.stress = max(0, min(100, self.stress))
        self.entertainment = max(0, min(100, self.entertainment))
        self.comfort = max(0, min(100, self.comfort))
        self.food_at_home = max(0, self.food_at_home)

    def is_work_hour(self, hour_of_day: int, day_of_week: int) -> bool:
        if day_of_week >= 5 and not self.p.weekend_worker:
            return False
        start = self.p.work_start
        end = self.p.work_end
        
        if start < end:
            return start <= hour_of_day < end
        else:
            return hour_of_day >= start or hour_of_day < end

    def state_for_llm(self) -> str:
        return (
            f"Energy: {self.energy}\n"
            f"Hunger: {self.hunger}\n"
            f"Social: {self.social}\n"
            f"Health: {self.health}\n"
            f"Stress: {self.stress}\n"
            f"Entertainment: {self.entertainment}\n"
            f"Comfort: {self.comfort}\n"
            f"Food at home (items): {self.food_at_home}\n"
            f"Wealth (0.0-1.0): {self.wealth:.2f}\n"
        )

    def persona_block(self) -> str:
        p = self.p.persona
        return (
            f"Name: {p.name} (Age: {p.age})\n"
            f"Job: {p.job}\n"
            f"Description: {p.description}\n"
        )

    def tick_needs(self, is_sleeping: bool = False):
        self.hunger += self.p.hunger_gain
        self.stress += self.p.stress_gain
        self.health -= self.p.health_loss

        if is_sleeping:
             pass 
        else:
            self.energy -= self.p.energy_loss
            self.social -= self.p.social_loss
            self.entertainment -= self.p.entertainment_loss
 
        if self.stress > 60 or self.health < 50:
            self.comfort -= 2
        elif self.stress < 30 and self.health > 70:
            self.comfort += 1

        self.clamp()

    def propose_locations(self, town) -> List[Tuple[str, str]]:
        hod = town.hour_of_day
        dow = town.day_of_week
        options: List[Tuple[str, str]] = []

        if town.hour_abs <= self.busy_until_abs_hour:
            return [(self.location, "Busy (talking), staying put.")]

        if town.is_night() or self.energy <= self.p.energy_sleep:
            options.append(("home", "Nighttime or low energy => go home to sleep."))
            return options

        if self.is_work_hour(hod, dow) and town.can_enter_location("work", agent=self):
             options.append(("work", "Work schedule => go to work."))
             return options 

        if self.hunger >= self.p.hunger_eat:
            if self.food_at_home > 0:
                options.append(("home", "Hungry + food at home => eat at home."))
            if town.can_enter_location("restaurant", agent=self):
                options.append(("restaurant", "Hungry => eat at restaurant."))
            if town.can_enter_location("cafe", agent=self):
                options.append(("cafe", "Hungry => eat at cafe."))
            if self.food_at_home <= 1 and town.can_enter_location("shop", agent=self):
                options.append(("shop", "Hungry + low food => buy groceries."))
        if self.social <= self.p.social_seek:
            if town.can_enter_location("park", agent=self):
                options.append(("park", "Lonely => meet people at park."))
            if town.can_enter_location("cafe", agent=self):
                options.append(("cafe", "Lonely => socialize at cafe."))
            if town.can_enter_location("bar", agent=self) and not town.is_night():
                options.append(("bar", "Lonely => socialize at bar."))
            if town.can_enter_location("restaurant", agent=self):
                options.append(("restaurant", "Lonely => dinner with others."))
            if town.can_enter_location("gym", agent=self):
                 options.append(("gym", "Lonely => gym is a social place."))
        if self.stress >= self.p.stress_seek_relief:
            if town.can_enter_location("park", agent=self):
                options.append(("park", "Stressed => relax in park."))
            if town.can_enter_location("library", agent=self):
                options.append(("library", "Stressed => quiet time at library."))
            if town.can_enter_location("gym", agent=self):
                options.append(("gym", "Stressed => exercise at gym."))
            if town.can_enter_location("bar", agent=self) and not town.is_night():
                options.append(("bar", "Stressed => unwind at bar."))
            if town.can_enter_location("home", agent=self):
                options.append(("home", "Stressed => relax at home."))
        if self.entertainment <= self.p.entertainment_seek:
            if town.can_enter_location("park", agent=self):
                options.append(("park", "Bored => fun at park."))
            if town.can_enter_location("library", agent=self):
                options.append(("library", "Bored => read at library."))
            if town.can_enter_location("bar", agent=self) and not town.is_night():
                options.append(("bar", "Bored => fun at bar."))
            if town.can_enter_location("restaurant", agent=self):
                options.append(("restaurant", "Bored => enjoy food at restaurant."))
            if town.can_enter_location("gym", agent=self):
                options.append(("gym", "Bored => activity at gym."))
            if town.can_enter_location("shop", agent=self):
                options.append(("shop", "Bored => go shopping."))
        if self.health <= self.p.health_seek_care:
             if town.can_enter_location("hospital", agent=self):
                options.append(("hospital", "Unwell => go to hospital."))
             if town.can_enter_location("gym", agent=self):
                options.append(("gym", "Unwell => light exercise."))
             if town.can_enter_location("park", agent=self):
                options.append(("park", "Unwell => fresh air."))
        if not options:
            options.append(("home", "Free time => stay home."))
            if town.can_enter_location("park", agent=self):
                options.append(("park", "Free time => walk in park."))
            if town.can_enter_location("library", agent=self):
                 options.append(("library", "Free time => browse library."))
            if town.can_enter_location("cafe", agent=self):
                 options.append(("cafe", "Free time => hang out at cafe."))
            if town.can_enter_location("gym", agent=self):
                 options.append(("gym", "Free time => workout."))
            if town.can_enter_location("bar", agent=self):
                 options.append(("bar", "Free time => socialize at bar."))
            if town.can_enter_location("restaurant", agent=self):
                 options.append(("restaurant", "Free time => enjoy meal out."))
            if town.can_enter_location("shop", agent=self):
                 options.append(("shop", "Free time => browse shops."))

        seen = set()
        uniq = []
        for loc, reason in options:
            if loc not in seen:
                uniq.append((loc, reason))
                seen.add(loc)        
        return uniq

    def choose_location(self, town) -> Tuple[str, str]:
        options = self.propose_locations(town)
            
        if len(options) == 1:
            loc, reason = options[0]
            print(f"[HARDCODED] {self.p.persona.name}: 1 option '{loc}' - {reason}")
            return options[0]

        valid_locs = [loc for (loc, _) in options]
        
        prompt = (
            "You are deciding where this agent goes next. Choose based on their personality and current state.\n"
            "Return ONLY this JSON format: {\"location\": \"exact_name_from_valid_location_names\", \"reason\": \"why_in_characters\"}\n\n"
            "IMPORTANT:\n"
            "- 'location' must EXACTLY match one of the valid names below\n"
            "- 'reason' should reflect this character's personality and feelings (1 sentence)\n\n"
            "- Do NOT mention raw numbers in the reason\n"
            "- Do NOT optimize like a game; choose what a human would realistically do\n\n"
            "- Prefer variety: if multiple options make sense, pick the more socially/plausibly interesting one.\n"
            "STATE INTERPRETATION (all are 0-100 unless noted):\n"
            "- Energy: low=exhausted, high=energized\n"
            "- Hunger: low=full, high=very hungry\n"
            "- Social: low=lonely, high=socially satisfied\n"
            "- Health: low=unwell, high=healthy\n"
            "- Stress: low=relaxed, high=overwhelmed\n"
            "- Entertainment: low=bored, high=entertained\n"
            "- Comfort: low=uncomfortable, high=comfortable\n"
            "- Food at home is a count of items; Wealth is 0.0-1.0 (higher=can afford more places)\n"
            "Use these mappings internally when writing the reason.\n\n"
            "=== WHO YOU ARE ===\n"
            f"{self.persona_block()}\n\n"
            "=== HOW YOU FEEL RIGHT NOW ===\n"
            f"{self.state_for_llm()}\n\n"
            f"Current location: {self.location}\n"
            f"Current time: Day {town.day_index}, {town.hour_of_day:02d}:00\n\n"
            f"Valid location names: {valid_locs}\n\n"
            "Your decision as JSON:"
        )

        data = self.llm.complete_json(prompt, max_tokens=100, stop=["\n"])
        loc = data.get("location")
        reason = data.get("reason", "Placeholder")

        if loc not in valid_locs:
            l0, r0 = options[0]
            raw = (data.get("raw") or "")[:200]
            print(f"[LLM FAIL] {self.p.persona.name}: Invalid location '{loc}'. Valid: {valid_locs}. Raw: {raw}")
            return l0, f"LLM invalid: {r0}"
        print(f"[LLM OK] {self.p.persona.name} chose: {loc} (from {len(options)} options)")
        return loc, reason

    def apply_location_effects(self, town=None):
        if town is not None:
            loc_obj = town.get_location(self.location)
            if loc_obj:
                self.energy += loc_obj.energy_change
                self.hunger += loc_obj.hunger_change
                self.social += loc_obj.social_change
                if self.location == "home":
                    if self.hunger >= 60 and self.food_at_home > 0:
                        self.food_at_home -= 1
                        self.hunger -= 45
                    self.stress -= 3
                    self.comfort += 2
                elif self.location == "shop":
                    self.food_at_home += 4
                    self.stress += 1
                elif self.location == "cafe" or self.location == "restaurant":
                    if self.hunger >= 55:
                        self.hunger -= 35
                    self.comfort += 1
                    self.entertainment += 1
                elif self.location == "park":
                    self.health += 1
                    self.stress -= 2
                    self.entertainment += 1
                elif self.location == "gym":
                    self.health += 3
                    self.stress -= 2
                    self.entertainment += 1
                elif self.location == "library":
                    self.stress -= 3
                    self.entertainment += 1
                elif self.location == "bar":
                    self.stress -= 3
                    self.entertainment += 3
                    self.health -= 1
                elif self.location == "work":
                    self.stress += 2
                    self.entertainment -= 1
                elif self.location == "hospital":
                    self.health += 5
                    self.stress -= 1
                
                self.clamp()
                return
       
        self.clamp()

    def wants_to_talk(self, location: str) -> bool:
        if location == "work" and not self.p.talk_at_work:
            return False
        if self.social > self.p.social_seek:
            return False
        return random.random() < self.p.sociability

    def after_talk(self, abs_hour: int):
        self.social += 25
        self.energy -= 1
        self.busy_until_abs_hour = max(self.busy_until_abs_hour, abs_hour + 1)
        self.clamp()
    
    def choose_location_no_llm(self, town) -> Tuple[str, str]:
        options = self.propose_locations(town)
            
        if len(options) == 1:
            loc, reason = options[0]
            print(f"[HARDCODED] {self.p.persona.name}: 1 option '{loc}' - {reason}")
            return options[0]
        return options[0]