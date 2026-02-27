"""Knowledge Nugget Generator for InsightFlow Kids"""

import random
from typing import Dict, List, Tuple, Optional


class KnowledgeNuggetGenerator:
    """Generate interesting facts and knowledge tidbits"""
    
    def __init__(self):
        self.nugget_database = self._load_nugget_database()
    
    def generate_nugget(self,
                       age_range: Tuple[int, int],
                       theme: str = "general",
                       interests: List[str] = None) -> Dict:
        """Generate an age-appropriate knowledge nugget"""
        
        # Filter nuggets by age and theme
        suitable_nuggets = self._filter_nuggets(age_range, theme, interests)
        
        if not suitable_nuggets:
            # Fallback to general nuggets
            suitable_nuggets = self._filter_nuggets(age_range, "general", None)
        
        nugget = random.choice(suitable_nuggets)
        
        # Add follow-up elements
        nugget["wonder_prompt"] = self._generate_wonder_prompt(nugget)
        nugget["activity"] = self._generate_activity(nugget, age_range[0])
        
        return nugget
    
    def _filter_nuggets(self, 
                       age_range: Tuple[int, int],
                       theme: str,
                       interests: List[str]) -> List[Dict]:
        """Filter nuggets based on criteria"""
        
        filtered = []
        theme_nuggets = self.nugget_database.get(theme, [])
        
        for nugget in theme_nuggets:
            if age_range[0] <= nugget["age_min"] <= age_range[1]:
                if interests:
                    # Bonus points for matching interests
                    if any(interest in nugget.get("tags", []) for interest in interests):
                        filtered.append(nugget)
                else:
                    filtered.append(nugget)
        
        return filtered
    
    def _generate_wonder_prompt(self, nugget: Dict) -> str:
        """Generate a wonder/thinking prompt based on the fact"""
        
        prompts = [
            f"What else do you wonder about {nugget.get('subject', 'this')}?",
            "Draw what you think this looks like!",
            "Can you think of something similar?",
            "What questions does this make you think of?",
            "How could we learn more about this?"
        ]
        
        return random.choice(prompts)
    
    def _generate_activity(self, nugget: Dict, age: int) -> Dict:
        """Generate a related activity"""
        
        activity_types = []
        
        if nugget.get("observable", False):
            activity_types.append({
                "type": "observation",
                "prompt": f"Look for {nugget['subject']} today!",
                "record": "Draw or describe what you see"
            })
        
        if nugget.get("testable", False):
            activity_types.append({
                "type": "experiment",
                "prompt": "Try this simple test:",
                "steps": nugget.get("experiment_steps", ["Observe", "Record", "Think"])
            })
        
        # Default creative activity
        activity_types.append({
            "type": "creative",
            "prompt": f"Imagine you are a {nugget.get('subject', 'scientist')}",
            "task": "What would your day be like?"
        })
        
        return random.choice(activity_types)
    
    def _load_nugget_database(self) -> Dict[str, List[Dict]]:
        """Load categorized knowledge nuggets"""
        
        return {
            "ocean": [
                {
                    "fact": "Octopuses have three hearts and blue blood!",
                    "subject": "octopuses",
                    "explanation": "Two hearts pump blood to their gills, and one pumps blood to the rest of their body.",
                    "age_min": 6,
                    "tags": ["animals", "biology", "weird"],
                    "observable": False,
                    "visual": "Draw an octopus with 3 hearts"
                },
                {
                    "fact": "The ocean is so deep that we've explored more of space than our own seas!",
                    "subject": "ocean exploration",
                    "explanation": "We've only explored about 5% of Earth's oceans.",
                    "age_min": 7,
                    "tags": ["exploration", "mystery"],
                    "testable": False
                },
                {
                    "fact": "Some fish can change colors like chameleons!",
                    "subject": "color-changing fish",
                    "explanation": "Flounder and cuttlefish can match their surroundings in seconds.",
                    "age_min": 5,
                    "tags": ["animals", "adaptation"],
                    "observable": True,
                    "experiment_steps": ["Find pictures of flounder", "See how they blend in", "Try to spot them!"]
                },
                {
                    "fact": "Dolphins have names for each other!",
                    "subject": "dolphins",
                    "explanation": "Each dolphin has a unique whistle that works like a name.",
                    "age_min": 6,
                    "tags": ["animals", "communication", "intelligence"],
                    "observable": False
                }
            ],
            
            "space": [
                {
                    "fact": "A day on Venus is longer than a year on Venus!",
                    "subject": "Venus",
                    "explanation": "Venus rotates so slowly that one day takes longer than its trip around the sun.",
                    "age_min": 7,
                    "tags": ["planets", "time", "weird"],
                    "observable": False
                },
                {
                    "fact": "You can see the International Space Station from your backyard!",
                    "subject": "the ISS",
                    "explanation": "It looks like a bright star moving steadily across the sky.",
                    "age_min": 6,
                    "tags": ["observation", "technology"],
                    "observable": True,
                    "experiment_steps": ["Check ISS tracker online", "Go outside at the right time", "Look for the moving 'star'"]
                },
                {
                    "fact": "Footprints on the Moon last forever!",
                    "subject": "Moon footprints",
                    "explanation": "There's no wind or rain to wash them away.",
                    "age_min": 5,
                    "tags": ["moon", "history"],
                    "testable": True,
                    "experiment_steps": ["Make footprint in sand", "Blow on it", "Now imagine no wind ever!"]
                },
                {
                    "fact": "Jupiter is so big that all other planets could fit inside it!",
                    "subject": "Jupiter",
                    "explanation": "It's like a giant vacuum cleaner protecting Earth from asteroids.",
                    "age_min": 6,
                    "tags": ["planets", "size", "protection"],
                    "observable": False
                }
            ],
            
            "science": [
                {
                    "fact": "Hot water can freeze faster than cold water!",
                    "subject": "the Mpemba effect",
                    "explanation": "Scientists still aren't sure exactly why this happens.",
                    "age_min": 7,
                    "tags": ["physics", "mystery", "water"],
                    "testable": True,
                    "experiment_steps": ["With adult help, try it!", "Use ice cube trays", "Time both trays"]
                },
                {
                    "fact": "Honey never goes bad - archaeologists found 3000-year-old honey that's still good!",
                    "subject": "honey",
                    "explanation": "Honey has special properties that prevent bacteria from growing.",
                    "age_min": 6,
                    "tags": ["food", "preservation", "history"],
                    "observable": True
                },
                {
                    "fact": "Your body has more bacterial cells than human cells!",
                    "subject": "bacteria",
                    "explanation": "But don't worry - most of them help keep you healthy!",
                    "age_min": 8,
                    "tags": ["biology", "health", "weird"],
                    "observable": False
                },
                {
                    "fact": "Plants can 'talk' to each other through their roots!",
                    "subject": "plant communication",
                    "explanation": "They send chemical signals to warn about dangers.",
                    "age_min": 7,
                    "tags": ["plants", "communication", "nature"],
                    "testable": False
                }
            ],
            
            "nature": [
                {
                    "fact": "Butterflies taste with their feet!",
                    "subject": "butterflies",
                    "explanation": "They land on plants to 'taste' if it's good for laying eggs.",
                    "age_min": 5,
                    "tags": ["insects", "senses", "adaptation"],
                    "observable": True,
                    "experiment_steps": ["Watch butterflies in garden", "See where they land", "Those might be tasty plants!"]
                },
                {
                    "fact": "Trees in a forest help each other by sharing food through their roots!",
                    "subject": "trees",
                    "explanation": "Big trees help feed baby trees through underground networks.",
                    "age_min": 6,
                    "tags": ["plants", "cooperation", "forest"],
                    "observable": False
                },
                {
                    "fact": "Some birds use tools just like humans!",
                    "subject": "clever birds",
                    "explanation": "Crows use sticks to get bugs, and some even make their own tools.",
                    "age_min": 6,
                    "tags": ["birds", "intelligence", "tools"],
                    "observable": True
                }
            ],
            
            "general": [
                {
                    "fact": "Your brain uses about the same power as a 10-watt light bulb!",
                    "subject": "your brain",
                    "explanation": "Even when you're sleeping, your brain is busy working.",
                    "age_min": 7,
                    "tags": ["body", "energy", "amazing"],
                    "observable": False
                },
                {
                    "fact": "The inventor of the Pringles can is buried in one!",
                    "subject": "Fredric Baur",
                    "explanation": "He was so proud of his invention, his ashes were buried in a Pringles can.",
                    "age_min": 7,
                    "tags": ["inventors", "funny", "history"],
                    "observable": False
                },
                {
                    "fact": "Bubble wrap was originally invented as wallpaper!",
                    "subject": "bubble wrap",
                    "explanation": "It failed as wallpaper but became perfect for protecting packages.",
                    "age_min": 6,
                    "tags": ["inventions", "accidents", "useful"],
                    "testable": True,
                    "experiment_steps": ["Feel bubble wrap", "Imagine it on walls", "Pop for science!"]
                }
            ]
        }


def generate_themed_nugget(theme: str, age: int) -> Dict:
    """Quick helper to generate a single nugget"""
    generator = KnowledgeNuggetGenerator()
    return generator.generate_nugget(
        age_range=(age - 1, age + 1),
        theme=theme
    )