"""Creative Prompt Generator for InsightFlow Kids"""

import random
from typing import Dict, List, Optional


class CreativePromptGenerator:
    """Generate creative activities and prompts"""
    
    def __init__(self):
        self.prompt_templates = self._load_templates()
    
    def generate_prompt(self, 
                       age: int, 
                       interests: List[str],
                       theme: str = "general") -> Dict:
        """Generate age-appropriate creative prompt"""
        
        # Select prompt type based on age
        if age <= 6:
            prompt_types = ["drawing", "simple_story", "imagination"]
        else:
            prompt_types = ["drawing", "story", "design", "invention", "poetry"]
        
        prompt_type = random.choice(prompt_types)
        
        if prompt_type == "drawing":
            return self._generate_drawing_prompt(age, theme)
        elif prompt_type == "story":
            return self._generate_story_prompt(age, theme)
        elif prompt_type == "design":
            return self._generate_design_prompt(theme)
        elif prompt_type == "invention":
            return self._generate_invention_prompt(theme)
        else:
            return self._generate_imagination_prompt(theme)
    
    def generate_collaborative_story(self, theme: str) -> Dict:
        """Generate a story-building activity for siblings"""
        
        starters = {
            "ocean": "A message in a bottle washed up on shore. Inside it said...",
            "space": "The spaceship's computer suddenly announced...",
            "adventure": "The old map showed a secret door that led to...",
            "science": "The experiment went wrong and suddenly...",
            "default": "Nobody expected what happened next..."
        }
        
        return {
            "type": "collaborative_story",
            "starter": starters.get(theme, starters["default"]),
            "rules": [
                "Take turns adding one sentence",
                "Each sentence must connect to the last one",
                "Try to use at least one word from today's theme",
                "End the story together after 10 sentences"
            ],
            "bonus": "Draw your favorite scene from the story!"
        }
    
    def _generate_drawing_prompt(self, age: int, theme: str) -> Dict:
        """Generate drawing prompts with constraints"""
        
        constraints = [
            "using only circles and squares",
            "without lifting your pencil",
            "using only 3 colors",
            "making it as silly as possible",
            "making it tiny in one corner",
            "filling the whole page"
        ]
        
        if theme == "ocean":
            subjects = ["an underwater castle", "a fish wearing clothes", 
                       "your dream submarine", "a mermaid's garden"]
        elif theme == "space":
            subjects = ["an alien's house", "a rocket made of food",
                       "Earth from the moon", "a space pet"]
        else:
            subjects = ["your perfect treehouse", "a machine that makes you happy",
                       "what clouds taste like", "your superhero self"]
        
        return {
            "type": "drawing",
            "prompt": f"Draw {random.choice(subjects)}",
            "constraint": random.choice(constraints),
            "extension": "Give your creation a name and one special power!"
        }
    
    def _generate_story_prompt(self, age: int, theme: str) -> Dict:
        """Generate story writing prompts"""
        
        if age <= 7:
            # Simple story starters
            prompts = [
                "My pet dragon is very small and lives in...",
                "When I shrunk to the size of an ant, I saw...",
                "The talking [animal] told me a secret..."
            ]
            word_limit = 50
        else:
            # More complex prompts
            prompts = [
                "You wake up and everyone else has vanished except...",
                "You discover you can talk to one type of object...",
                "A door appears in your room that wasn't there yesterday..."
            ]
            word_limit = 100
        
        return {
            "type": "story",
            "prompt": random.choice(prompts),
            "constraints": [
                f"Use exactly {word_limit} words",
                f"Include something {theme}-related",
                "Give your main character an unusual problem"
            ],
            "story_helper": "Beginning → Problem → Solution → End"
        }
    
    def _generate_design_prompt(self, theme: str) -> Dict:
        """Generate design challenges"""
        
        challenges = {
            "ocean": "Design a house for a fish family",
            "space": "Design a playground for aliens",
            "science": "Design a robot that helps with chores",
            "default": "Design a new type of vehicle"
        }
        
        return {
            "type": "design",
            "challenge": challenges.get(theme, challenges["default"]),
            "requirements": [
                "Label 3 important parts",
                "Explain what makes it special",
                "Include one impossible feature"
            ],
            "bonus": "What would you name your design?"
        }
    
    def _generate_invention_prompt(self, theme: str) -> Dict:
        """Generate invention challenges"""
        
        problems = [
            "waking up on time is hard",
            "remembering things is tricky",
            "cleaning up is boring",
            "waiting is difficult",
            "finding lost things takes forever"
        ]
        
        return {
            "type": "invention",
            "problem": f"Problem: {random.choice(problems)}",
            "task": "Invent something to solve this problem!",
            "include": [
                "Draw your invention",
                "Name it",
                "List 3 things it does",
                "One silly feature it has"
            ]
        }
    
    def _generate_imagination_prompt(self, theme: str) -> Dict:
        """Generate open-ended imagination prompts"""
        
        prompts = [
            "If you could mix any two animals together...",
            "If your toys came alive at night...",
            "If you could eat clouds...",
            "If you had a magic paintbrush...",
            "If your backyard was a different planet..."
        ]
        
        return {
            "type": "imagination",
            "prompt": random.choice(prompts),
            "explore": [
                "What would happen?",
                "What would it look like?",
                "What rules would change?",
                "Draw or write your ideas!"
            ]
        }
    
    def _load_templates(self) -> Dict:
        """Load creative prompt templates"""
        return {
            "drawing_subjects": {
                "characters": ["wizard", "robot", "explorer", "inventor", "creature"],
                "places": ["castle", "laboratory", "jungle", "city", "island"],
                "objects": ["machine", "vehicle", "tool", "treasure", "portal"]
            },
            "story_elements": {
                "problems": ["lost something important", "needs to save a friend",
                           "discovers a secret", "must solve a puzzle", "goes on quest"],
                "helpers": ["wise owl", "magic map", "friendly ghost", "talking animal",
                          "mysterious stranger"],
                "solutions": ["teamwork", "clever thinking", "kindness", "bravery",
                            "imagination"]
            }
        }