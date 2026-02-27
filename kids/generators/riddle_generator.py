"""Riddle Generator for InsightFlow Kids"""

import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RiddleType(Enum):
    WHAT_AM_I = "what_am_i"
    WORDPLAY = "wordplay"
    LOGIC = "logic"
    MATH = "math"
    LATERAL = "lateral_thinking"


@dataclass
class Riddle:
    """A complete riddle with metadata"""
    question: str
    answer: str
    hint: Optional[str] = None
    explanation: Optional[str] = None
    riddle_type: RiddleType = RiddleType.WHAT_AM_I
    difficulty: int = 1  # 1-5 scale
    themes: List[str] = None


class RiddleGenerator:
    """Generate age-appropriate riddles with various difficulty levels"""
    
    def __init__(self):
        self.riddle_database = self._load_riddle_database()
        self.riddle_templates = self._load_templates()
    
    def generate_riddle_set(self, 
                          count: int = 3,
                          min_difficulty: int = 1,
                          max_difficulty: int = 3,
                          theme: Optional[str] = None) -> List[Riddle]:
        """Generate a set of riddles with progressive difficulty"""
        riddles = []
        
        # Ensure progressive difficulty
        difficulties = sorted([random.randint(min_difficulty, max_difficulty) 
                             for _ in range(count)])
        
        # Get riddles from database
        available_riddles = self._filter_riddles(theme, min_difficulty, max_difficulty)
        
        # Mix database riddles with generated ones
        for i, difficulty in enumerate(difficulties):
            if random.random() < 0.7 and available_riddles:
                # Use database riddle
                suitable = [r for r in available_riddles 
                          if abs(r.difficulty - difficulty) <= 1]
                if suitable:
                    riddle = random.choice(suitable)
                    available_riddles.remove(riddle)
                    riddles.append(riddle)
                    continue
            
            # Generate new riddle
            riddle = self._generate_riddle(difficulty, theme)
            riddles.append(riddle)
        
        return riddles
    
    def generate_collaborative_riddle(self) -> Tuple[str, str, str]:
        """Generate a riddle that requires two people to solve"""
        templates = [
            (
                "I have two parts that must unite. One child sees day, one sees night. "
                "Put your clues together right, and my identity comes to light.",
                "Part 1 (Child A): I shine bright in the sky by day.",
                "Part 2 (Child B): I glow softly in the sky by night.",
                "Answer: The sky (contains both sun and moon)"
            ),
            (
                "We're a pair that works as one, separately we're not much fun. "
                "One of you knows what we do, the other knows what we're made of too.",
                "Part 1 (Child A): We help you walk and run and play.",
                "Part 2 (Child B): We're made of leather, rubber, and lace.",
                "Answer: Shoes"
            )
        ]
        
        return random.choice(templates)
    
    def _generate_riddle(self, difficulty: int, theme: Optional[str] = None) -> Riddle:
        """Generate a new riddle based on templates"""
        riddle_type = self._select_riddle_type(difficulty)
        
        if riddle_type == RiddleType.WHAT_AM_I:
            return self._generate_what_am_i(difficulty, theme)
        elif riddle_type == RiddleType.MATH:
            return self._generate_math_riddle(difficulty)
        elif riddle_type == RiddleType.WORDPLAY:
            return self._generate_wordplay_riddle(difficulty)
        elif riddle_type == RiddleType.LOGIC:
            return self._generate_logic_riddle(difficulty)
        else:
            return self._generate_lateral_riddle(difficulty)
    
    def _generate_what_am_i(self, difficulty: int, theme: Optional[str] = None) -> Riddle:
        """Generate a 'What Am I?' riddle"""
        
        if difficulty <= 2:
            # Simple, concrete objects
            templates = [
                ("I have hands but cannot clap. I have a face but cannot see. "
                 "I help you know when to eat and sleep. What am I?",
                 "A clock",
                 "Think about what tells time"),
                
                ("I'm full of holes but can hold water. "
                 "I help you clean but get dirty. What am I?",
                 "A sponge",
                 "Found in the kitchen or bathroom"),
                
                ("I have teeth but cannot bite. I help make you neat and tidy. "
                 "You use me every morning. What am I?",
                 "A comb",
                 "Look in the bathroom")
            ]
        else:
            # More abstract concepts
            templates = [
                ("I can be cracked, made, told, and played. "
                 "I bring smiles but I'm not a toy. What am I?",
                 "A joke",
                 "Think about what makes people laugh"),
                
                ("The more you take, the more you leave behind. "
                 "I help you go places without a car. What am I?",
                 "Footsteps",
                 "Think about walking"),
                
                ("I have cities but no houses, forests but no trees, "
                 "water but no fish. What am I?",
                 "A map",
                 "It shows places but isn't real")
            ]
        
        question, answer, hint = random.choice(templates)
        return Riddle(
            question=question,
            answer=answer,
            hint=hint,
            riddle_type=RiddleType.WHAT_AM_I,
            difficulty=difficulty,
            themes=[theme] if theme else []
        )
    
    def _generate_math_riddle(self, difficulty: int) -> Riddle:
        """Generate a mathematical riddle"""
        
        if difficulty <= 2:
            # Simple counting/addition
            num1 = random.randint(2, 5)
            num2 = random.randint(2, 5)
            total = num1 + num2
            
            question = (f"I have {num1} red balloons and {num2} blue balloons. "
                       f"How many balloons do I have in total?")
            answer = str(total)
            hint = "Count them all together"
            
        else:
            # Pattern or multiplication
            base = random.randint(2, 4)
            
            question = (f"Every day, the number of flowers in my garden doubles. "
                       f"I start with {base} flowers on Monday. "
                       f"How many will I have on Wednesday?")
            answer = str(base * 4)  # Double twice
            hint = f"Monday: {base}, Tuesday: ?, Wednesday: ?"
        
        return Riddle(
            question=question,
            answer=answer,
            hint=hint,
            explanation=f"Let's work through it: {hint}",
            riddle_type=RiddleType.MATH,
            difficulty=difficulty
        )
    
    def _generate_wordplay_riddle(self, difficulty: int) -> Riddle:
        """Generate a wordplay-based riddle"""
        
        if difficulty <= 2:
            templates = [
                ("What has 'tea' in it but you can't drink?",
                 "Teacher",
                 "Someone who helps you learn"),
                
                ("What word starts with 'e', ends with 'e', "
                 "but only has one letter in it?",
                 "Envelope",
                 "Mail goes inside it")
            ]
        else:
            templates = [
                ("What word becomes shorter when you add two letters to it?",
                 "Short",
                 "Add 'er' to make 'shorter'"),
                
                ("I'm pronounced as one letter but written with three. "
                 "Two letters there are, and two only in me. "
                 "I'm double, I'm single, I'm black, blue, and gray. "
                 "I'm read from both ends and the same either way.",
                 "Eye",
                 "You see with it")
            ]
        
        question, answer, hint = random.choice(templates)
        return Riddle(
            question=question,
            answer=answer,
            hint=hint,
            riddle_type=RiddleType.WORDPLAY,
            difficulty=difficulty
        )
    
    def _generate_logic_riddle(self, difficulty: int) -> Riddle:
        """Generate a logic-based riddle"""
        
        if difficulty <= 2:
            question = ("Three fish are in a tank. One swims away. "
                       "How many are left in the tank?")
            answer = "Three"
            explanation = "Fish can't swim out of a tank!"
        else:
            question = ("A farmer has 17 sheep. All but 9 run away. "
                       "How many are left?")
            answer = "Nine"
            explanation = "'All but 9' means 9 stayed"
        
        return Riddle(
            question=question,
            answer=answer,
            explanation=explanation,
            riddle_type=RiddleType.LOGIC,
            difficulty=difficulty
        )
    
    def _generate_lateral_riddle(self, difficulty: int) -> Riddle:
        """Generate a lateral thinking riddle"""
        
        templates = [
            ("A man lives on the 20th floor of a building. "
             "Every day he takes the elevator down. "
             "When he comes home, he takes the elevator to the 10th floor "
             "and walks the rest. Why?",
             "He's too short to reach the button for the 20th floor",
             "Think about why he can't use all the buttons"),
            
            ("You see a boat filled with people. "
             "You look again and now it's empty but it hasn't sunk. How?",
             "All the people were married (not single/empty)",
             "Think about the word 'single'")
        ]
        
        question, answer, hint = random.choice(templates)
        return Riddle(
            question=question,
            answer=answer,
            hint=hint,
            riddle_type=RiddleType.LATERAL,
            difficulty=max(3, difficulty)  # These are always harder
        )
    
    def _select_riddle_type(self, difficulty: int) -> RiddleType:
        """Select appropriate riddle type based on difficulty"""
        if difficulty <= 2:
            return random.choice([
                RiddleType.WHAT_AM_I,
                RiddleType.WHAT_AM_I,  # More weight
                RiddleType.MATH,
                RiddleType.WORDPLAY
            ])
        else:
            return random.choice([
                RiddleType.WHAT_AM_I,
                RiddleType.LOGIC,
                RiddleType.WORDPLAY,
                RiddleType.LATERAL
            ])
    
    def _filter_riddles(self, theme: Optional[str], 
                       min_diff: int, max_diff: int) -> List[Riddle]:
        """Filter riddles from database"""
        filtered = []
        
        for riddle in self.riddle_database:
            if min_diff <= riddle.difficulty <= max_diff:
                if theme is None or theme in riddle.themes:
                    filtered.append(riddle)
        
        return filtered
    
    def _load_riddle_database(self) -> List[Riddle]:
        """Load pre-written riddles"""
        return [
            Riddle(
                question="I fly without wings, I cry without eyes. "
                        "Whenever I go, darkness flies. What am I?",
                answer="A cloud",
                hint="Look up at the sky",
                riddle_type=RiddleType.WHAT_AM_I,
                difficulty=2,
                themes=["nature", "weather"]
            ),
            Riddle(
                question="What has a head and a tail but no body?",
                answer="A coin",
                hint="Check your pocket",
                riddle_type=RiddleType.WHAT_AM_I,
                difficulty=1,
                themes=["objects", "money"]
            ),
            Riddle(
                question="I'm tall when I'm young and short when I'm old. What am I?",
                answer="A candle",
                hint="I give light",
                riddle_type=RiddleType.WHAT_AM_I,
                difficulty=2,
                themes=["objects", "light"]
            ),
            # Add more riddles to database as needed
        ]
    
    def _load_templates(self) -> Dict:
        """Load riddle generation templates"""
        return {
            "what_am_i": {
                "parts": [
                    "I have {feature1} but no {feature2}",
                    "I can be {state1} or {state2}",
                    "You use me to {action}",
                    "I'm found in {location}"
                ]
            }
        }


def generate_daily_riddles(child1_age: int, child2_age: int) -> Dict[str, List[Riddle]]:
    """Generate riddles for both children"""
    generator = RiddleGenerator()
    
    # Calculate difficulty ranges
    child1_min = max(1, (child1_age - 5))
    child1_max = min(5, (child1_age - 3))
    
    child2_min = max(1, (child2_age - 5))
    child2_max = min(5, (child2_age - 3))
    
    # Generate sets
    result = {
        "shared": generator.generate_riddle_set(
            count=2, 
            min_difficulty=min(child1_min, child2_min),
            max_difficulty=min(child1_max, child2_max)
        ),
        "dahlia": generator.generate_riddle_set(
            count=1,
            min_difficulty=child1_min,
            max_difficulty=child1_max
        ),
        "xander": generator.generate_riddle_set(
            count=1,
            min_difficulty=child2_min,
            max_difficulty=child2_max
        )
    }
    
    # Add collaborative riddle on some days
    if random.random() < 0.3:  # 30% chance
        collab = generator.generate_collaborative_riddle()
        result["collaborative"] = collab
    
    return result