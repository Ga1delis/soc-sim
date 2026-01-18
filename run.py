import random
from agents.agent import Agent, AgentProfile, Persona
from env.town import Town
from llm.client import LLMClient
from memory.store import MemoryStore
from simlog.logger import SimLogger
from simulation.conversation import ConversationManager

from typing import List

DOW_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def get_all_agent_profiles() -> List[AgentProfile]:
    profiles = []

    p_asta = Persona("Asta", 28, "nurse", "A dedicated and compassionate nurse who has lived in this town her whole life. She is known for her patience and warm smile, but she struggles with taking time for herself. Deeply family-oriented, she loves cooking traditional meals and hosting Sunday dinners, though she often feels exhausted by the emotional toll of her job.")
    profiles.append(AgentProfile(persona=p_asta, work_start=7, work_end=19, weekend_worker=True, hunger_gain=6, energy_loss=2, social_loss=3, stress_gain=5, sociability=0.8, wealth_level=0.55, health_seek_care=70, energy_sleep=35, stress_seek_relief=55))

    p_mantas = Persona("Mantas", 34, "engineer", "A methodical and highly analytical civil engineer. He approaches life like a project, always optimizing his schedule and resources. He is introverted but polite, preferring deep one-on-one technical discussions over small talk. In his free time, he is an avid cyclist and coffee connoisseur, often seen analyzing the structural integrity of his espresso foam.")
    profiles.append(AgentProfile(persona=p_mantas, work_start=9, work_end=17, hunger_gain=5, energy_loss=2, social_loss=2, stress_gain=4, sociability=0.4, wealth_level=0.75, talk_at_work=True, social_seek=40, stress_seek_relief=70, entertainment_seek=30))

    p_ieva = Persona("Ieva", 22, "student", "A bubbling source of energy and the town's unofficial social coordinator. She is studying sociology and is endlessly fascinated by people's stories. She can be a bit scattering and disorganized, frequently late to everything, but her infectious enthusiasm makes her instantly forgiven. She lives for music festivals and spontaneous adventures.")
    profiles.append(AgentProfile(persona=p_ieva, work_start=8, work_end=15, hunger_gain=7, energy_loss=2, social_loss=6, stress_gain=3, sociability=0.95, wealth_level=0.2, social_seek=75, entertainment_seek=60, stress_seek_relief=65))

    p_tomas = Persona("Tomas", 41, "shop owner", "The skeptical owner of the town's main general store. He has seen it all and trusts very little of it. He is short with his words, brutally honest, and purely business-focused, yet he quietly looks out for the regulars. He worries constantly about inventory and margins, making him perpetually low-level stressed.")
    profiles.append(AgentProfile(persona=p_tomas, work_start=8, work_end=18, weekend_worker=True, hunger_gain=5, energy_loss=2, social_loss=2, stress_gain=5, sociability=0.6, wealth_level=0.6, talk_at_work=True, stress_seek_relief=50, social_seek=50, hunger_eat=65))

    p_rokas = Persona("Rokas", 26, "delivery driver", "A hyper-active adrenaline junkie who treats every delivery like a time-trial race. He is restless, loud, and constantly fidgeting. He loves gaming and talking about cars. He has zero attention span for serious topics but is the first to help if something needs moving physically. He essentially never walks anywhere; he runs.")
    profiles.append(AgentProfile(persona=p_rokas,work_start=10, work_end=20, weekend_worker=True, hunger_gain=9, energy_loss=3, social_loss=3, stress_gain=2, sociability=0.7, wealth_level=0.4, hunger_eat=60, entertainment_seek=55, stress_seek_relief=70))

    p_ruta = Persona("Rūta", 27, "yoga instructor", "The embodiment of calm in human form. She speaks softly and moves gracefully. She is deeply spiritual and believes in the interconnectedness of all living things. While some find her 'woo-woo' talk annoying, her presence is undeniably soothing. She spends most of her income on organic tea and sustainable clothing.")
    profiles.append(AgentProfile(persona=p_ruta, work_start=7, work_end=15, hunger_gain=4, energy_loss=2, social_loss=3, stress_gain=1, sociability=0.7, wealth_level=0.5, stress_seek_relief=75, health_seek_care=65, social_seek=50))

    p_jonas = Persona("Jonas", 38, "banker", "An old-fashioned gentleman who values tradition, propriety, and a well-tailored suit. He is extremely risk-averse and meticulously organized. He finds comfort in rules and clear expectations. He is polite to a fault but struggles to connect on an emotional level, often hiding behind formalities.")
    profiles.append(AgentProfile(persona=p_jonas, work_start=9, work_end=17, hunger_gain=5, energy_loss=2, social_loss=2, stress_gain=4, wealth_level=0.9, sociability=0.5, stress_seek_relief=55, social_seek=45, hunger_eat=75))

    p_gabija = Persona("Gabija", 25, "photographer", "A dreamy observer who sees the world through a lens of light and shadow. She often zones out in the middle of conversations because she noticed a beautiful reflection. She wanders aimlessly for hours, capturing the mundane beauty of the town. She is gentle, sensitive, and easily overwhelmed by loud noises.")
    profiles.append(AgentProfile(persona=p_gabija, work_start=10, work_end=16, weekend_worker=True, hunger_gain=5, energy_loss=2, social_loss=4, sociability=0.7, wealth_level=0.5, stress_seek_relief=55, social_seek=50, entertainment_seek=45))

    p_andrius = Persona("Andrius", 42, "police officer", "A figure of authority who takes his responsibility to protect the town very seriously. He is firm, alert, and physically imposing, yet he has a soft spot for kids and dogs. He values order and discipline above all else and can be judgmental of those he perceives as 'slackers'.")
    profiles.append(AgentProfile(persona=p_andrius, work_start=8, work_end=20, weekend_worker=True, hunger_gain=7, energy_loss=3, social_loss=3, stress_gain=4, sociability=0.6, wealth_level=0.65, stress_seek_relief=65, hunger_eat=65, social_seek=45))

    p_martynas = Persona("Martynas", 31, "musician", "A passionate and emotional artist who wears his heart on his sleeve. He lives a nocturnal lifestyle and comes alive when the sun goes down. He is charismatic and charming but prone to dramatic mood swings. He believes life is meaningless without art and expression.")
    profiles.append(AgentProfile(persona=p_martynas, work_start=19, work_end=3, weekend_worker=True, hunger_gain=6, energy_loss=2, social_loss=6, sociability=0.9, wealth_level=0.4, entertainment_seek=65, social_seek=70, stress_seek_relief=55, energy_sleep=20))

    p_lukas = Persona("Lukas", 29, "chef", "A culinary perfectionist with a fiery temper and an obsession with quality ingredients. He works grueling hours and demands the same intensity from everyone around him. He is loud, opinionated, and intensely critical, but his food is undeniably brilliant. He relieves stress by shouting.")
    profiles.append(AgentProfile(persona=p_lukas, work_start=11, work_end=23, weekend_worker=True, hunger_gain=7, energy_loss=3, social_loss=3, stress_gain=6, wealth_level=0.6, sociability=0.7, stress_seek_relief=45, hunger_eat=65, energy_sleep=30))

    p_egle = Persona("Eglė", 45, "librarian", "The keeper of the town's history and silence. She is incredibly shy and prefers the company of fictional characters to real ones. She speaks in a whisper and is easily startled. She is meticulous, organized, and deeply knowledgeable, acting as a hidden resource for anyone who takes the time to ask.")
    profiles.append(AgentProfile(persona=p_egle, work_start=9, work_end=17, hunger_gain=3, energy_loss=2, social_loss=2, stress_gain=2, sociability=0.3, wealth_level=0.5, social_seek=35, stress_seek_relief=70, entertainment_seek=30))

    p_simona = Persona("Simona", 23, "barista", "The bubbly face of the morning for everyone in town. She is impossibly cheerful at 6 AM and knows everyone's coffee order by heart. She loves gossip, fashion, and pop culture. She is constantly checking her phone and knows everything happening in town before it even happens.")
    profiles.append(AgentProfile(persona=p_simona, work_start=6, work_end=14, weekend_worker=True, hunger_gain=6, energy_loss=2, social_loss=7, sociability=0.95, wealth_level=0.3, social_seek=80, entertainment_seek=60))

    p_paulius = Persona("Paulius", 68, "retired", "A wise old soul who spends his days observing the town from park benches. He moves slowly and speaks with a deliberate, thoughtful cadence. He loves to tell long, winding stories about the 'good old days'. He is content, patient, and a calming presence for the younger, busier generations.")
    profiles.append(AgentProfile(persona=p_paulius, work_start=-1, work_end=-1, hunger_gain=4, energy_loss=2, social_loss=4, sociability=0.8, wealth_level=0.6, weekend_worker=False, energy_sleep=40, stress_seek_relief=80, social_seek=55))

    p_viktorija = Persona("Viktorija", 30, "software developer", "A highly intelligent but socially awkward programmer. She views social interactions as complex algorithms that she hasn't quite cracked yet. She is direct, literal, and often misses sarcasm. She stays up late coding and often forgets to eat. She respects competence above all else.")
    profiles.append(AgentProfile(persona=p_viktorija, work_start=10, work_end=18, hunger_gain=5, energy_loss=3, social_loss=2, stress_gain=3, sociability=0.3, wealth_level=0.8, social_seek=35, hunger_eat=80, entertainment_seek=30, stress_seek_relief=65))

    return profiles

def main():
    #Init objects
    model_path = "models/mistral-7b-instruct-v0.3-q4_k_m.gguf"
    llm = LLMClient(model_path=model_path, n_ctx=2048, n_threads=16, temperature=0.5, verbose=False)

    town = Town()
    mem = MemoryStore()
    log = SimLogger()
    conv = ConversationManager(llm=llm, memory_store=mem)

    print(f"Logs: {log.run_dir}")
    print(f"Agent init.")

    profiles = get_all_agent_profiles()
    agents = []
    for p in profiles:
        a = Agent(profile=p, memory_store=mem, llm=llm)
        agents.append(a)
        town.add_agent(a, "home")

    print(f"Amount of agents: {len(agents)}.")
    HOURS = 48
    for _ in range(HOURS):
        day = town.day_index
        hour = town.hour_of_day
        dow = town.day_of_week
        dow_name = DOW_NAMES[dow]

        counts = {loc: len(lst) for loc, lst in town.locations.items()}
        print(f"[Day {day} {dow_name} {hour:02d}:00] {counts}")
        log.log({"type": "time", "day": day, "hour": hour, "dow": dow, "dow_name": dow_name})

        # Select next step, update needs
        for a in agents:
            is_sleeping = False
            if town.is_night() and a.location == "home":
                is_sleeping = True
            elif a.energy <= a.p.energy_sleep and a.location == "home":
                is_sleeping = True

            a.tick_needs(is_sleeping=is_sleeping)

            new_loc, reason = a.choose_location(town)
            #new_loc, reason = a.choose_location_no_llm(town)
            old_loc = a.location

            town.move_agent(a, new_loc)
            a.apply_location_effects(town)

            log.log({
                "type": "move",
                "day": day, "hour": hour, "dow": dow, "dow_name": dow_name,
                "agent": a.p.persona.name,
                "from": old_loc,
                "to": new_loc,
                "reason": reason,
                "attributes": {
                    "energy": a.energy,
                    "hunger": a.hunger,
                    "social": a.social,
                    "health": a.health,
                    "stress": a.stress,
                    "entertainment": a.entertainment,
                    "comfort": a.comfort,
                    "food_at_home": a.food_at_home,
                    "wealth": a.wealth
                }
            })
        # Manage conversation
        used_agents = set()
        for location_name, people_here in town.locations.items():
            if location_name == "home":
                continue
            if len(people_here) < 2:
                continue
            random.shuffle(people_here)

            for agent_a in people_here:
                if agent_a.p.persona.name in used_agents:
                    continue
                if not agent_a.wants_to_talk(location_name):
                    continue

                potential_partners = [
                    p for p in people_here 
                    if p.p.persona.name != agent_a.p.persona.name 
                    and p.p.persona.name not in used_agents
                    and p.wants_to_talk(location_name)
                ]
                
                if not potential_partners:
                    continue

                agent_b = random.choice(potential_partners)
                used_agents.add(agent_a.p.persona.name)
                used_agents.add(agent_b.p.persona.name)
                transcript = conv.run_conversation(agent_a, agent_b, location=location_name, day=day, hour=hour, dow=dow)
                #transcript = conv.run_conversation_no_llm(
                #    agent_a, agent_b, location=location_name,
                #    day=day, hour=hour, dow=dow,
                #)
                agent_a.after_talk(town.hour_abs)
                agent_b.after_talk(town.hour_abs)
                conv.store_conversation_memory(agent_a, agent_b, location_name, transcript)

                log.log({
                    "type": "dialogue",
                    "day": day, "hour": hour, "dow": dow, 
                    "location": location_name,
                    "agent_a": agent_a.p.persona.name,
                    "agent_b": agent_b.p.persona.name,
                    "turn_count": len(transcript),
                    "transcript": transcript,
                })
                first_line = transcript[0]['text'] if transcript else "..."
                print(f"{location_name}: {agent_a.p.persona.name} and {agent_b.p.persona.name} | {first_line}")
        town.step_time()

    print("Finish.")

if __name__ == "__main__":
    main()
