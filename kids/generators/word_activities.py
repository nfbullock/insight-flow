"""Word Activity Generator for InsightFlow Kids"""

import random
import string
from typing import Dict, List, Optional, Tuple


class WordActivityGenerator:
    """Generate various word-based activities"""
    
    def __init__(self):
        self.word_lists = self._load_word_lists()
    
    def generate_activity(self,
                         activity_type: str,
                         difficulty: float,
                         theme: str = "general") -> Dict:
        """Generate specified word activity"""
        
        generators = {
            "word_ladder": self._generate_word_ladder,
            "word_ladder_simple": lambda d, t: self._generate_word_ladder(d, t, simple=True),
            "mini_crossword": self._generate_mini_crossword,
            "word_search": self._generate_word_search,
            "anagrams": self._generate_anagrams,
            "rhyme_time": self._generate_rhyme_time,
            "letter_patterns": self._generate_letter_patterns
        }
        
        generator = generators.get(activity_type, self._generate_word_ladder)
        return generator(difficulty, theme)
    
    def _generate_word_ladder(self, difficulty: float, theme: str, 
                             simple: bool = False) -> Dict:
        """Generate word ladder puzzle"""
        
        if simple:
            # 3-letter words for younger kids
            ladders = [
                ("CAT", "DOG", ["CAT", "COT", "DOT", "DOG"]),
                ("SUN", "FUN", ["SUN", "SUN", "FUN"]),
                ("BAT", "HAT", ["BAT", "HAT"])
            ]
        else:
            # 4-letter words for older kids
            ladders = [
                ("SHIP", "BOAT", ["SHIP", "SHOP", "SHOT", "BOOT", "BOAT"]),
                ("COLD", "WARM", ["COLD", "CORD", "WORD", "WORM", "WARM"]),
                ("FISH", "SEAL", ["FISH", "FIST", "FEST", "FEAT", "SEAT", "SEAL"])
            ]
        
        if theme == "ocean":
            # Pick ocean-themed ladder if available
            ladder = ladders[0] if not simple else ladders[0]
        else:
            ladder = random.choice(ladders)
        
        start_word, end_word, solution = ladder
        
        return {
            "type": "word_ladder",
            "start": start_word,
            "end": end_word,
            "length": len(solution) - 2,  # Intermediate steps
            "hint": f"Change one letter at a time to get from {start_word} to {end_word}",
            "solution": solution,
            "display_solution": False
        }
    
    def _generate_mini_crossword(self, difficulty: float, theme: str) -> Dict:
        """Generate small crossword puzzle"""
        
        size = 5 if difficulty > 2 else 4
        
        # Simplified crossword data
        if theme == "ocean":
            words = {
                "across": [
                    {"word": "WAVE", "clue": "Ocean movement", "start": (0, 0)},
                    {"word": "FISH", "clue": "Swims in water", "start": (2, 0)}
                ],
                "down": [
                    {"word": "WHALE", "clue": "Big ocean animal", "start": (0, 0)},
                    {"word": "SHIP", "clue": "Boat", "start": (0, 3)}
                ]
            }
        else:
            words = {
                "across": [
                    {"word": "PLAY", "clue": "Have fun", "start": (0, 0)},
                    {"word": "GAME", "clue": "Fun activity", "start": (2, 1)}
                ],
                "down": [
                    {"word": "PAGE", "clue": "Part of a book", "start": (0, 0)},
                    {"word": "LIME", "clue": "Green fruit", "start": (1, 1)}
                ]
            }
        
        return {
            "type": "mini_crossword",
            "size": size,
            "words": words,
            "instruction": "Fill in the words using the clues"
        }
    
    def _generate_word_search(self, difficulty: float, theme: str) -> Dict:
        """Generate word search puzzle"""
        
        size = 8 if difficulty > 2 else 6
        
        # Theme-based word lists
        word_lists = {
            "ocean": ["FISH", "WAVE", "SAND", "BOAT", "SWIM"],
            "space": ["STAR", "MOON", "ROCKET", "PLANET", "ORBIT"],
            "general": ["PLAY", "READ", "JUMP", "SING", "DRAW"]
        }
        
        words = word_lists.get(theme, word_lists["general"])
        
        # Add easier/harder words based on difficulty
        if difficulty <= 2:
            words = words[:4]  # Fewer, shorter words
        
        return {
            "type": "word_search",
            "size": size,
            "words": words,
            "directions": ["horizontal", "vertical"] if difficulty <= 2 else 
                         ["horizontal", "vertical", "diagonal"],
            "instruction": "Find all the hidden words!"
        }
    
    def _generate_anagrams(self, difficulty: float, theme: str) -> Dict:
        """Generate anagram puzzles"""
        
        # Word sets by difficulty
        if difficulty <= 2:
            anagrams = [
                ("TAC", "CAT", "Animal that says meow"),
                ("TOP", "POT", "Used for cooking"),
                ("TAR", "ART", "Drawing and painting")
            ]
        else:
            anagrams = [
                ("PARTS", "STRAP", "Holds things together"),
                ("LEAST", "STEAL", "Take without asking"),
                ("EARTH", "HEART", "Beats in your chest")
            ]
        
        puzzles = []
        for scrambled, answer, clue in random.sample(anagrams, min(3, len(anagrams))):
            puzzles.append({
                "scrambled": scrambled,
                "clue": clue,
                "answer": answer
            })
        
        return {
            "type": "anagrams",
            "puzzles": puzzles,
            "instruction": "Unscramble the letters to find the word!"
        }
    
    def _generate_rhyme_time(self, difficulty: float, theme: str) -> Dict:
        """Generate rhyming activities"""
        
        rhyme_families = {
            "simple": [
                {"word": "cat", "rhymes": ["hat", "bat", "mat", "sat", "rat"]},
                {"word": "sun", "rhymes": ["fun", "run", "bun", "done", "won"]},
                {"word": "cake", "rhymes": ["make", "take", "bake", "lake", "wake"]}
            ],
            "medium": [
                {"word": "light", "rhymes": ["night", "fight", "bright", "might", "sight"]},
                {"word": "round", "rhymes": ["sound", "found", "ground", "pound", "bound"]}
            ]
        }
        
        family = random.choice(rhyme_families["simple"] if difficulty <= 2 else rhyme_families["medium"])
        
        return {
            "type": "rhyme_time",
            "base_word": family["word"],
            "find_count": 3 if difficulty <= 2 else 5,
            "hint": f"Find words that rhyme with {family['word']}",
            "bonus": "Make up a silly sentence using 2 rhyming words!"
        }
    
    def _generate_letter_patterns(self, difficulty: float, theme: str) -> Dict:
        """Generate letter pattern recognition"""
        
        patterns = []
        
        if difficulty <= 2:
            # Simple patterns
            patterns.extend([
                {
                    "sequence": ["A", "B", "A", "B", "?"],
                    "answer": "A",
                    "rule": "Alternating letters"
                },
                {
                    "sequence": ["C", "D", "E", "F", "?"],
                    "answer": "G",
                    "rule": "Alphabet order"
                }
            ])
        else:
            # Complex patterns
            patterns.extend([
                {
                    "sequence": ["A", "C", "E", "G", "?"],
                    "answer": "I",
                    "rule": "Skip one letter each time"
                },
                {
                    "sequence": ["Z", "Y", "X", "W", "?"],
                    "answer": "V",
                    "rule": "Backwards alphabet"
                }
            ])
        
        selected = random.sample(patterns, min(2, len(patterns)))
        
        return {
            "type": "letter_patterns",
            "patterns": selected,
            "instruction": "What letter comes next?",
            "bonus": "Create your own pattern for someone else to solve!"
        }
    
    def _load_word_lists(self) -> Dict:
        """Load categorized word lists"""
        return {
            "three_letter": ["cat", "dog", "sun", "fun", "bat", "hat", "run", "big"],
            "four_letter": ["ship", "boat", "fish", "wave", "star", "moon", "play", "game"],
            "five_letter": ["ocean", "space", "world", "dream", "smile", "laugh", "dance"],
            "theme_words": {
                "ocean": ["sea", "wave", "fish", "boat", "swim", "sand", "shell", "deep"],
                "space": ["star", "moon", "mars", "rocket", "alien", "orbit", "planet"],
                "nature": ["tree", "bird", "flower", "grass", "cloud", "rain", "snow"]
            }
        }