import random
from typing import Dict, List

class ConversationManager:
    def __init__(self, llm, memory_store=None):
        self.llm = llm
        self.memory = memory_store

    def decide_turns(self, a, b, location: str) -> int:
        base_turns = random.randint(4, 8)
        if a.social < 30 and b.social < 30:
            base_turns += 2
        if location in ["restaurant", "bar", "cafe"]:
            base_turns += 2
        return base_turns

    def _mem_snippet(self, agent_name: str) -> str:
        if not self.memory:
            return "no memory"
        data = self.memory.load(agent_name)
        summary = data.get("summary", "")
        facts = data.get("facts", [])[-4:]
        
        out = []
        if summary:
            out.append(f"Summary: {summary}")
        if facts:
            out.append("Recent facts:")
            out.extend([f"- {f}" for f in facts])
        
        return "\n".join(out) if out else "no memory"

    def prompt_turn(self, speaker, listener, location: str, day: int, hour: int, dow: int, transcript: List[Dict[str, str]]) -> str:
        last = transcript[-6:]
        convo = "\n".join([f"{t['speaker']}: {t['text']}" for t in last]) if last else "(start of conversation)"

        speaker_mem = self._mem_snippet(speaker.p.persona.name)

        prompt = (
            "You are roleplaying a specific person in a town simulation.\n"
            f"You are {speaker.p.persona.name}. You are talking to {listener.p.persona.name}.\n\n"
            "CRITICAL RULES:\n"
            f"1. Write ONLY {speaker.p.persona.name}'s dialogue. DO NOT write {listener.p.persona.name}'s response.\n"
            "2. Keep responses natural and conversational (2-4 sentences).\n\n"
            "=== YOUR IDENTITY ===\n"
            f"{speaker.persona_block()}\n\n"
            "=== CURRENT STATE ===\n"
            f"{speaker.state_for_llm()}\n"
            f"Location: {location} | Time: {hour:02d}:00\n"
            f"Relevant Memory: {speaker_mem}\n\n"
            "=== CONVERSATION HISTORY ===\n"
            f"{convo}\n\n"
            f"{speaker.p.persona.name}:"
        )
        return prompt
    
    def run_conversation(self, a, b, location: str, day: int, hour: int, dow: int) -> List[Dict[str, str]]:
        turns = self.decide_turns(a, b, location)
        transcript: List[Dict[str, str]] = []   

        speaker, listener = a, b
        stop = [f"\n{a.p.persona.name}:", f"\n{b.p.persona.name}:", "\n==="]
        for _ in range(turns):
            prompt = self.prompt_turn(speaker, listener, location, day, hour, dow, transcript)
            raw = self.llm.complete(prompt, max_tokens=100, stop=stop).strip()

            if not raw:
                raw = "..."

            transcript.append({"speaker": speaker.p.persona.name, "text": raw})
            speaker, listener = listener, speaker

        return transcript

    def summarize_interaction(self, a, b, location: str, transcript: List[Dict[str, str]]) -> str:
        full_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in transcript])
        prompt = (
            "Summarize this conversation into ONE sentence from the perspective of an observer.\n"
            "Focus on the main topic.\n"
            f"Participants: {a.p.persona.name} and {b.p.persona.name}\n"
            f"Location: {location}\n\n"
            "=== TRANSCRIPT ===\n"
            f"{full_text}\n\n"
            "Summary:"
        )
        summary = self.llm.complete(prompt, max_tokens=60, stop=["\n"]).strip()
        return summary

    def store_conversation_memory(self, a, b, location: str, transcript: List[Dict[str, str]]):
        if not self.memory:
            return
        summary_text = self.summarize_interaction(a, b, location, transcript)

        self.memory.add_fact(a.p.persona.name, f"Met {b.p.persona.name} at {location}. {summary_text}")
        self.memory.add_fact(b.p.persona.name, f"Met {a.p.persona.name} at {location}. {summary_text}")
        data_a = self.memory.load(a.p.persona.name)
        data_b = self.memory.load(b.p.persona.name)
        
        new_sum_a = (data_a.get("summary", "") + "\n" + f"- {summary_text}").strip()
        new_sum_b = (data_b.get("summary", "") + "\n" + f"- {summary_text}").strip()
        if len(new_sum_a) > 1200:
            new_sum_a = "..." + new_sum_a[-1200:]
        if len(new_sum_b) > 1200:
            new_sum_b = "..." + new_sum_b[-1200:]
        data_a["summary"] = new_sum_a
        data_b["summary"] = new_sum_b
        self.memory.save(a.p.persona.name, data_a)
        self.memory.save(b.p.persona.name, data_b)

    def run_conversation_no_llm(self, a, b, location: str, day: int, hour: int, dow: int, abs_hour: int) -> List[Dict[str, str]]:
        turns = self.decide_turns(a, b, location)
        transcript: List[Dict[str, str]] = []

        speaker, listener = a, b
        transcript.append({"speaker": speaker.p.persona.name, "text": "placeholder"})
        speaker, listener = listener, speaker

        return transcript