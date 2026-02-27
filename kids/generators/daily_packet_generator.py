"""Daily Packet Generator - Orchestrates all content for a day"""

import json
import random
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from logic_puzzle_generator import LogicPuzzleGenerator, Difficulty, generate_puzzle_pair
from riddle_generator import RiddleGenerator, generate_daily_riddles
from creative_prompts import CreativePromptGenerator
from word_activities import WordActivityGenerator
from math_challenges import MathChallengeGenerator
from knowledge_nuggets import KnowledgeNuggetGenerator


@dataclass
class ChildProfile:
    """Profile tracking for each child"""
    name: str
    age: int
    grade: int
    academic_level: float  # Grade level for academics
    interests: List[str]
    recent_themes: List[str]  # Last 7 days
    completion_history: Dict[str, List[float]]  # activity_type: success_rates
    current_focus_areas: List[str]
    collaboration_score: float  # 0-1, how well they work together


@dataclass
class DailyPacket:
    """Complete content for one day"""
    date: str
    child_name: str
    theme: str
    activities: List[Dict[str, Any]]
    collaborative_activities: List[Dict[str, Any]]
    parent_notes: str
    tomorrow_teaser: str
    special_elements: Optional[List[Dict[str, Any]]] = None


class DailyPacketGenerator:
    """Orchestrates generation of complete daily packets"""
    
    def __init__(self, profiles_dir: str = "profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        
        # Initialize content generators
        self.logic_gen = LogicPuzzleGenerator()
        self.riddle_gen = RiddleGenerator()
        self.creative_gen = CreativePromptGenerator()
        self.word_gen = WordActivityGenerator()
        self.math_gen = MathChallengeGenerator()
        self.knowledge_gen = KnowledgeNuggetGenerator()
        
        # Theme rotation
        self.themes = {
            0: "adventure",    # Monday
            1: "science",      # Tuesday  
            2: "creative",     # Wednesday
            3: "history",      # Thursday
            4: "free-choice",  # Friday
            5: "exploration",  # Saturday
            6: "reflection"    # Sunday
        }
    
    def generate_daily_packets(self, 
                             for_date: Optional[date] = None) -> Dict[str, DailyPacket]:
        """Generate packets for all children"""
        if for_date is None:
            for_date = date.today()
        
        # Load profiles
        dahlia = self.load_profile("dahlia")
        xander = self.load_profile("xander")
        
        # Determine theme
        theme = self._select_theme(for_date, dahlia, xander)
        
        # Generate shared collaborative content
        collaborative = self._generate_collaborative_content(dahlia, xander, theme)
        
        # Generate individual packets
        packets = {
            "dahlia": self._generate_packet(dahlia, for_date, theme, collaborative),
            "xander": self._generate_packet(xander, for_date, theme, collaborative)
        }
        
        # Update profiles with today's content
        self._update_profiles(dahlia, xander, theme)
        
        return packets
    
    def _generate_packet(self, 
                        profile: ChildProfile, 
                        packet_date: date,
                        theme: str,
                        collaborative: List[Dict]) -> DailyPacket:
        """Generate packet for one child"""
        
        activities = []
        
        # 1. Morning Password (collaborative warm-up)
        activities.append(self._generate_morning_password(theme))
        
        # 2. Logic Puzzle (adapted to level)
        logic_difficulty = self._get_difficulty(profile)
        logic_puzzle = self.logic_gen.generate_puzzle(logic_difficulty, theme)
        activities.append({
            "type": "logic_puzzle",
            "content": asdict(logic_puzzle),
            "estimated_time": 10 if profile.age <= 6 else 12
        })
        
        # 3. Creative Activity
        creative = self.creative_gen.generate_prompt(
            age=profile.age,
            interests=profile.interests,
            theme=theme
        )
        activities.append({
            "type": "creative",
            "content": creative,
            "estimated_time": 15
        })
        
        # 4. Word Activity (alternating types)
        word_activity = self._select_word_activity(profile, theme)
        activities.append({
            "type": "word_activity", 
            "content": word_activity,
            "estimated_time": 8
        })
        
        # 5. Math Challenge (level-appropriate)
        math = self.math_gen.generate_challenge(
            grade_level=profile.academic_level,
            theme=theme,
            visual=profile.age <= 6
        )
        activities.append({
            "type": "math",
            "content": math,
            "estimated_time": 10
        })
        
        # 6. Knowledge Nugget
        nugget = self.knowledge_gen.generate_nugget(
            age_range=(profile.age - 1, profile.age + 1),
            theme=theme,
            interests=profile.interests
        )
        activities.append({
            "type": "knowledge",
            "content": nugget,
            "estimated_time": 5
        })
        
        # 7. Daily Reflection
        reflection = self._generate_reflection_prompts(profile)
        activities.append({
            "type": "reflection",
            "content": reflection,
            "estimated_time": 5
        })
        
        # Add riddles throughout
        riddles = generate_daily_riddles(8 if profile.name == "dahlia" else 6, 6)
        self._distribute_riddles(activities, riddles[profile.name.lower()])
        
        # Generate metadata
        parent_notes = self._generate_parent_notes(activities, profile)
        tomorrow_teaser = self._generate_teaser(packet_date, theme)
        
        # Special elements for special days
        special = self._check_special_elements(packet_date, profile)
        
        return DailyPacket(
            date=packet_date.isoformat(),
            child_name=profile.name,
            theme=theme,
            activities=activities,
            collaborative_activities=collaborative,
            parent_notes=parent_notes,
            tomorrow_teaser=tomorrow_teaser,
            special_elements=special
        )
    
    def _generate_collaborative_content(self, 
                                      profile1: ChildProfile,
                                      profile2: ChildProfile,
                                      theme: str) -> List[Dict]:
        """Generate activities requiring both children"""
        collaborative = []
        
        # Shared logic puzzle with split clues
        logic1, logic2 = generate_puzzle_pair(
            self._get_difficulty(profile1),
            self._get_difficulty(profile2),
            theme
        )
        
        if logic1.collaborative_clues:
            collaborative.append({
                "type": "split_logic_puzzle",
                "content": {
                    "base_puzzle": asdict(logic1),
                    "child1_clues": logic1.collaborative_clues[0],
                    "child2_clues": logic1.collaborative_clues[1],
                    "instructions": "Each of you has special clues! Work together to solve."
                }
            })
        
        # Collaborative story building
        if random.random() < 0.3:  # 30% chance
            collaborative.append({
                "type": "story_building",
                "content": self.creative_gen.generate_collaborative_story(theme)
            })
        
        # Team challenge
        if random.random() < 0.4:  # 40% chance
            collaborative.append({
                "type": "team_challenge",
                "content": self._generate_team_challenge(theme)
            })
        
        return collaborative
    
    def _generate_morning_password(self, theme: str) -> Dict:
        """Generate the morning unlock puzzle"""
        passwords = {
            "ocean": ["SWIM LIKE DOLPHINS", "TREASURE HUNTERS", "DEEP SEA DANCE"],
            "space": ["ROCKET LAUNCH", "MOON WALKING", "STAR JUMPERS"],
            "adventure": ["BRAVE EXPLORERS", "QUEST BEGINS", "ADVENTURE TIME"],
            "science": ["MAD SCIENTISTS", "EXPERIMENT TIME", "DISCOVERY DANCE"],
            "creative": ["IMAGINATION STATION", "CREATE AND PLAY", "ART ATTACK"],
            "history": ["TIME TRAVELERS", "ANCIENT SECRETS", "HISTORY DETECTIVES"],
            "default": ["MORNING MAGIC", "BRAIN POWER", "READY TO LEARN"]
        }
        
        password_list = passwords.get(theme, passwords["default"])
        password = random.choice(password_list)
        
        # Create simple rebus or code
        puzzle_types = ["rebus", "number_code", "picture_decode"]
        puzzle_type = random.choice(puzzle_types)
        
        if puzzle_type == "rebus":
            clues = self._create_rebus(password)
        elif puzzle_type == "number_code":
            clues = self._create_number_code(password)
        else:
            clues = self._create_picture_decode(password)
        
        return {
            "type": "morning_password",
            "content": {
                "puzzle": clues,
                "answer": password,
                "action": f"Do this together: {password}!",
                "hint": "Work together to decode today's password"
            }
        }
    
    def _select_word_activity(self, profile: ChildProfile, theme: str) -> Dict:
        """Select appropriate word activity"""
        if profile.age <= 6:
            activities = ["word_ladder_simple", "rhyme_time", "letter_patterns"]
        else:
            activities = ["word_ladder", "mini_crossword", "word_search", "anagrams"]
        
        activity_type = random.choice(activities)
        
        return self.word_gen.generate_activity(
            activity_type=activity_type,
            difficulty=profile.academic_level,
            theme=theme
        )
    
    def _generate_reflection_prompts(self, profile: ChildProfile) -> Dict:
        """Generate age-appropriate reflection questions"""
        base_prompts = [
            "What made your brain grow today?",
            "What was the most fun part?",
            "What do you want to try tomorrow?"
        ]
        
        if profile.age >= 8:
            base_prompts.extend([
                "What strategy helped you solve the hardest puzzle?",
                "How did you help your sibling today?",
                "What would you change about today's activities?"
            ])
        
        return {
            "prompts": random.sample(base_prompts, 3),
            "rating": "Circle: 😄 😐 😟",
            "favorite": "⭐ Star your favorite activity!",
            "learned": "One new thing I learned: __________"
        }
    
    def _generate_team_challenge(self, theme: str) -> Dict:
        """Generate a challenge requiring teamwork"""
        challenges = {
            "ocean": {
                "title": "Design an Underwater City",
                "task": "One person draws buildings, the other draws sea creatures. "
                       "Create a complete underwater world together!",
                "bonus": "Give your city a name and make up 3 rules for living there."
            },
            "space": {
                "title": "Space Mission Planning", 
                "task": "Plan a mission to a new planet. One person lists what to bring, "
                       "the other draws the spaceship. Work together!",
                "bonus": "What would you name your spaceship?"
            },
            "default": {
                "title": "Invention Time",
                "task": "Invent something that doesn't exist yet. One person describes it, "
                       "the other draws it. Make it amazing!",
                "bonus": "What problem does your invention solve?"
            }
        }
        
        return challenges.get(theme, challenges["default"])
    
    def _distribute_riddles(self, activities: List[Dict], riddles: List) -> None:
        """Insert riddles between main activities"""
        # Add riddles at positions 3 and 5 (after logic puzzle and math)
        if len(riddles) >= 2:
            activities.insert(3, {
                "type": "riddle",
                "content": asdict(riddles[0]),
                "estimated_time": 3
            })
            activities.insert(6, {
                "type": "riddle", 
                "content": asdict(riddles[1]),
                "estimated_time": 3
            })
    
    def _generate_parent_notes(self, activities: List, profile: ChildProfile) -> str:
        """Generate notes for parents"""
        total_time = sum(a.get("estimated_time", 0) for a in activities)
        
        notes = f"Today's Packet Overview:\n"
        notes += f"- Total time: ~{total_time} minutes\n"
        notes += f"- Focus areas: "
        
        focus = set()
        for activity in activities:
            if activity["type"] == "logic_puzzle":
                focus.add("logical reasoning")
            elif activity["type"] == "creative":
                focus.add("creative expression")
            elif activity["type"] == "math":
                focus.add("mathematical thinking")
        
        notes += ", ".join(focus) + "\n"
        notes += f"- Collaboration opportunities: Check split activities\n"
        notes += f"\nDinner conversation starter: Ask about today's password!"
        
        return notes
    
    def _generate_teaser(self, packet_date: date, current_theme: str) -> str:
        """Generate excitement for tomorrow"""
        tomorrow = packet_date + datetime.timedelta(days=1)
        tomorrow_theme = self.themes[tomorrow.weekday()]
        
        teasers = {
            "adventure": "Tomorrow: A mysterious map appears...",
            "science": "Tomorrow: Explosive science experiments!",
            "creative": "Tomorrow: Become an artist extraordinaire!",
            "history": "Tomorrow: Travel back in time!",
            "free-choice": "Tomorrow: Friday fun surprises!",
            "exploration": "Tomorrow: Weekend adventure special!",
            "reflection": "Tomorrow: Share your week's discoveries!"
        }
        
        return teasers.get(tomorrow_theme, "Tomorrow: New adventures await!")
    
    def _check_special_elements(self, 
                              packet_date: date, 
                              profile: ChildProfile) -> Optional[List[Dict]]:
        """Check for special occasions"""
        special = []
        
        # Birthday check
        # This would need actual birthday data
        # if is_birthday(packet_date, profile):
        #     special.append(generate_birthday_special(profile))
        
        # Holiday check
        # if is_holiday(packet_date):
        #     special.append(generate_holiday_activity(packet_date))
        
        # Milestone check (e.g., 30 days of packets)
        # if check_milestone(profile):
        #     special.append(generate_milestone_celebration(profile))
        
        return special if special else None
    
    def _get_difficulty(self, profile: ChildProfile) -> Difficulty:
        """Map profile to difficulty enum"""
        if profile.academic_level <= 2:
            return Difficulty.K2
        elif profile.academic_level <= 5:
            return Difficulty.G35
        else:
            return Difficulty.G68
    
    def _select_theme(self, 
                     packet_date: date, 
                     profile1: ChildProfile,
                     profile2: ChildProfile) -> str:
        """Select theme avoiding recent repetition"""
        base_theme = self.themes[packet_date.weekday()]
        
        if base_theme == "free-choice":
            # Pick based on interests and recent themes
            all_interests = set(profile1.interests + profile2.interests)
            recent = set(profile1.recent_themes + profile2.recent_themes)
            
            available = all_interests - recent
            if available:
                return random.choice(list(available))
        
        return base_theme
    
    def _update_profiles(self, 
                        profile1: ChildProfile, 
                        profile2: ChildProfile,
                        theme: str) -> None:
        """Update profiles with today's theme"""
        for profile in [profile1, profile2]:
            profile.recent_themes.append(theme)
            if len(profile.recent_themes) > 7:
                profile.recent_themes.pop(0)
            
            self.save_profile(profile)
    
    def load_profile(self, name: str) -> ChildProfile:
        """Load child profile from disk"""
        profile_path = self.profiles_dir / f"{name}.json"
        
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                data = json.load(f)
                return ChildProfile(**data)
        else:
            # Create default profile
            if name.lower() == "dahlia":
                return ChildProfile(
                    name="Dahlia",
                    age=8,
                    grade=2,
                    academic_level=3.5,
                    interests=["ocean", "mysteries", "art", "stories"],
                    recent_themes=[],
                    completion_history={},
                    current_focus_areas=["emotional_vocabulary", "social_scenarios"],
                    collaboration_score=0.8
                )
            else:
                return ChildProfile(
                    name="Xander",
                    age=6,
                    grade=0,
                    academic_level=2.0,
                    interests=["space", "building", "patterns", "animals"],
                    recent_themes=[],
                    completion_history={},
                    current_focus_areas=["writing_stamina", "reading_comprehension"],
                    collaboration_score=0.75
                )
    
    def save_profile(self, profile: ChildProfile) -> None:
        """Save profile to disk"""
        profile_path = self.profiles_dir / f"{profile.name.lower()}.json"
        with open(profile_path, 'w') as f:
            json.dump(asdict(profile), f, indent=2)
    
    def _create_rebus(self, password: str) -> List[Dict]:
        """Create picture-based puzzle"""
        # Simplified rebus creation
        words = password.split()
        clues = []
        
        for word in words:
            if word == "SWIM":
                clues.append({"type": "picture", "desc": "🏊"})
            elif word == "LIKE":
                clues.append({"type": "picture", "desc": "👍"})
            # ... etc for other words
            else:
                clues.append({"type": "text", "desc": word[0] + "???"})
        
        return clues
    
    def _create_number_code(self, password: str) -> Dict:
        """Create number substitution cipher"""
        # A=1, B=2, etc.
        return {
            "type": "number_code",
            "numbers": [ord(c) - ord('A') + 1 if c != ' ' else 0 
                       for c in password],
            "hint": "A=1, B=2, C=3..."
        }
    
    def _create_picture_decode(self, password: str) -> List[Dict]:
        """Create picture decoding puzzle"""
        # This would have actual picture logic in production
        return [
            {"type": "picture_sequence", "hint": "First letters spell the password"}
        ]


# Placeholder imports for other generators
# These would be separate files in production
class CreativePromptGenerator:
    def generate_prompt(self, age: int, interests: List[str], theme: str) -> Dict:
        return {"prompt": "Draw your perfect day!", "constraints": ["Use only circles"]}
    
    def generate_collaborative_story(self, theme: str) -> Dict:
        return {"start": "Once upon a time...", "rules": ["Take turns adding sentences"]}


class WordActivityGenerator:
    def generate_activity(self, activity_type: str, difficulty: float, theme: str) -> Dict:
        return {"type": activity_type, "content": "Sample word activity"}


class MathChallengeGenerator:
    def generate_challenge(self, grade_level: float, theme: str, visual: bool) -> Dict:
        return {"problem": "2 + 2 = ?", "visual_aid": visual}


class KnowledgeNuggetGenerator:
    def generate_nugget(self, age_range: tuple, theme: str, interests: List[str]) -> Dict:
        return {"fact": "The ocean is really deep!", "wonder": "What lives at the bottom?"}


if __name__ == "__main__":
    # Test generation
    generator = DailyPacketGenerator()
    packets = generator.generate_daily_packets()
    
    print("Generated packets for:", list(packets.keys()))
    print("\nDahlia's first activity:", packets["dahlia"].activities[0])