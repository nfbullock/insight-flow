"""Logic Grid Puzzle Generator for InsightFlow Kids"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    K2 = "k-2"  # Kindergarten to 2nd grade
    G35 = "3-5"  # Grades 3-5
    G68 = "6-8"  # Grades 6-8


@dataclass
class LogicPuzzle:
    """Complete logic puzzle with grid, clues, and solution"""
    title: str
    theme: str
    grid_size: int
    entities: List[str]
    attributes: Dict[str, List[str]]
    clues: List[str]
    solution: Dict[str, Dict[str, str]]
    difficulty: Difficulty
    collaborative_clues: Optional[Tuple[List[str], List[str]]] = None


class LogicPuzzleGenerator:
    """Generate age-appropriate logic grid puzzles with themes kids love"""
    
    def __init__(self):
        self.themes = self._load_themes()
        self.clue_templates = self._load_clue_templates()
    
    def generate_puzzle(self, 
                       difficulty: Difficulty,
                       theme: Optional[str] = None,
                       collaborative: bool = False) -> LogicPuzzle:
        """Generate a complete logic puzzle"""
        
        # Select theme
        if theme is None:
            theme = random.choice(list(self.themes.keys()))
        theme_data = self.themes[theme]
        
        # Determine grid size based on difficulty
        grid_size = {
            Difficulty.K2: 3,
            Difficulty.G35: 4,
            Difficulty.G68: 5
        }[difficulty]
        
        # Select entities and attributes
        entities = random.sample(theme_data['entities'], grid_size)
        attributes = {}
        for attr_name, attr_values in theme_data['attributes'].items():
            attributes[attr_name] = random.sample(attr_values, grid_size)
        
        # Generate solution
        solution = self._generate_solution(entities, attributes)
        
        # Generate clues
        if collaborative:
            clues, collab_clues = self._generate_collaborative_clues(
                solution, entities, attributes, difficulty
            )
            collaborative_clues = collab_clues
        else:
            clues = self._generate_clues(solution, entities, attributes, difficulty)
            collaborative_clues = None
        
        # Create title
        title = self._generate_title(theme, theme_data.get('title_templates', []))
        
        return LogicPuzzle(
            title=title,
            theme=theme,
            grid_size=grid_size,
            entities=entities,
            attributes=attributes,
            clues=clues,
            solution=solution,
            difficulty=difficulty,
            collaborative_clues=collaborative_clues
        )
    
    def _generate_solution(self, 
                          entities: List[str], 
                          attributes: Dict[str, List[str]]) -> Dict[str, Dict[str, str]]:
        """Create a valid solution grid"""
        solution = {entity: {} for entity in entities}
        
        # For each attribute type, create a random assignment
        for attr_name, attr_values in attributes.items():
            shuffled_values = attr_values.copy()
            random.shuffle(shuffled_values)
            
            for i, entity in enumerate(entities):
                solution[entity][attr_name] = shuffled_values[i]
        
        return solution
    
    def _generate_clues(self, 
                       solution: Dict[str, Dict[str, str]], 
                       entities: List[str],
                       attributes: Dict[str, List[str]],
                       difficulty: Difficulty) -> List[str]:
        """Generate clues based on difficulty level"""
        clues = []
        
        if difficulty == Difficulty.K2:
            # Direct, simple clues
            clues.extend(self._generate_direct_clues(solution, 3))
            clues.extend(self._generate_negative_clues(solution, entities, attributes, 2))
        
        elif difficulty == Difficulty.G35:
            # Mix of direct and relational clues
            clues.extend(self._generate_direct_clues(solution, 2))
            clues.extend(self._generate_relational_clues(solution, entities, attributes, 3))
            clues.extend(self._generate_negative_clues(solution, entities, attributes, 2))
        
        else:  # G68
            # Complex relational and conditional clues
            clues.extend(self._generate_direct_clues(solution, 1))
            clues.extend(self._generate_relational_clues(solution, entities, attributes, 3))
            clues.extend(self._generate_conditional_clues(solution, entities, attributes, 2))
            clues.extend(self._generate_complex_clues(solution, entities, attributes, 2))
        
        random.shuffle(clues)
        return clues
    
    def _generate_collaborative_clues(self,
                                    solution: Dict[str, Dict[str, str]], 
                                    entities: List[str],
                                    attributes: Dict[str, List[str]],
                                    difficulty: Difficulty) -> Tuple[List[str], Tuple[List[str], List[str]]]:
        """Generate clues where each child gets exclusive information"""
        
        # Generate base clues
        all_clues = self._generate_clues(solution, entities, attributes, difficulty)
        
        # Keep some shared clues
        shared_count = len(all_clues) // 2
        shared_clues = all_clues[:shared_count]
        
        # Split remaining clues
        remaining = all_clues[shared_count:]
        mid_point = len(remaining) // 2
        
        child1_exclusive = remaining[:mid_point]
        child2_exclusive = remaining[mid_point:]
        
        # Add collaborative hint
        shared_clues.append("💡 Compare your clues with your sibling to find the solution!")
        
        return shared_clues, (child1_exclusive, child2_exclusive)
    
    def _generate_direct_clues(self, solution: Dict, count: int) -> List[str]:
        """Generate simple direct assignment clues"""
        clues = []
        items = [(e, a, v) for e, attrs in solution.items() 
                 for a, v in attrs.items()]
        
        for entity, attr, value in random.sample(items, min(count, len(items))):
            clues.append(f"The {entity} has {value}.")
        
        return clues
    
    def _generate_negative_clues(self, solution: Dict, entities: List, 
                               attributes: Dict, count: int) -> List[str]:
        """Generate negative clues (X is not Y)"""
        clues = []
        
        for _ in range(count):
            entity = random.choice(entities)
            attr_name = random.choice(list(attributes.keys()))
            correct_value = solution[entity][attr_name]
            wrong_values = [v for v in attributes[attr_name] if v != correct_value]
            
            if wrong_values:
                wrong_value = random.choice(wrong_values)
                clues.append(f"The {entity} does not have {wrong_value}.")
        
        return clues
    
    def _generate_relational_clues(self, solution: Dict, entities: List,
                                 attributes: Dict, count: int) -> List[str]:
        """Generate clues about relationships between entities"""
        clues = []
        
        for _ in range(count):
            attr_name = random.choice(list(attributes.keys()))
            e1, e2 = random.sample(entities, 2)
            v1 = solution[e1][attr_name]
            v2 = solution[e2][attr_name]
            
            if random.random() < 0.5:
                # Positive relationship
                clues.append(f"The one with {v1} is not the {e2}.")
            else:
                # Different attributes
                if len(attributes) > 1:
                    attr_names = list(attributes.keys())
                    a1, a2 = random.sample(attr_names, 2)
                    v1 = solution[e1][a1]
                    v2 = solution[e1][a2]
                    clues.append(f"The one with {v1} also has {v2}.")
        
        return clues
    
    def _generate_conditional_clues(self, solution: Dict, entities: List,
                                  attributes: Dict, count: int) -> List[str]:
        """Generate if-then style clues"""
        clues = []
        
        for _ in range(count):
            e1, e2 = random.sample(entities, 2)
            attr = random.choice(list(attributes.keys()))
            v1 = solution[e1][attr]
            v2 = solution[e2][attr]
            
            clues.append(f"If the {e1} has {v1}, then the {e2} does not have {v2}.")
        
        return clues
    
    def _generate_complex_clues(self, solution: Dict, entities: List,
                              attributes: Dict, count: int) -> List[str]:
        """Generate complex multi-entity clues"""
        clues = []
        
        for _ in range(count):
            attr = random.choice(list(attributes.keys()))
            ents = random.sample(entities, 3)
            values = [solution[e][attr] for e in ents]
            
            clues.append(
                f"Between the {ents[0]}, {ents[1]}, and {ents[2]}, "
                f"one has {values[0]}, one has {values[1]}, "
                f"but not necessarily in that order."
            )
        
        return clues
    
    def _generate_title(self, theme: str, templates: List[str]) -> str:
        """Generate a fun, engaging title"""
        if templates:
            return random.choice(templates)
        
        defaults = [
            f"The {theme.title()} Mystery",
            f"{theme.title()} Mix-Up",
            f"Solving the {theme.title()} Puzzle",
            f"The Great {theme.title()} Challenge"
        ]
        return random.choice(defaults)
    
    def _load_themes(self) -> Dict:
        """Load puzzle themes"""
        return {
            "ocean": {
                "entities": ["dolphin", "shark", "octopus", "seahorse", "whale", 
                           "starfish", "crab", "jellyfish"],
                "attributes": {
                    "colors": ["blue", "gray", "orange", "pink", "purple", 
                             "yellow", "red", "green"],
                    "homes": ["coral reef", "deep ocean", "shallow water", 
                            "rocky shore", "kelp forest", "open sea", "tide pool", "shipwreck"],
                    "treasures": ["pearl", "shell", "coin", "gem", "crown", 
                                "map", "chest", "key"]
                },
                "title_templates": [
                    "Underwater Adventure",
                    "Ocean Friends Mystery",
                    "Deep Sea Detective"
                ]
            },
            "space": {
                "entities": ["astronaut", "alien", "robot", "scientist", "captain",
                           "engineer", "pilot", "explorer"],
                "attributes": {
                    "planets": ["Mars", "Venus", "Jupiter", "Saturn", "Neptune",
                              "Mercury", "Pluto", "Earth"],
                    "ships": ["Rocket", "Shuttle", "Probe", "Station", "Rover",
                            "Satellite", "Pod", "Cruiser"],
                    "discoveries": ["crater", "rings", "moon", "comet", "asteroid",
                                  "galaxy", "star", "nebula"]
                },
                "title_templates": [
                    "Space Station Puzzle",
                    "Galactic Mystery",
                    "Astronaut Assignment"
                ]
            },
            "pets": {
                "entities": ["dog", "cat", "hamster", "bird", "fish", "rabbit",
                           "turtle", "guinea pig"],
                "attributes": {
                    "names": ["Max", "Luna", "Charlie", "Bella", "Milo", "Daisy",
                            "Oliver", "Sophie"],
                    "toys": ["ball", "rope", "wheel", "bell", "tunnel", "stick",
                           "mirror", "swing"],
                    "colors": ["brown", "white", "black", "spotted", "striped",
                             "golden", "gray", "mixed"]
                },
                "title_templates": [
                    "Pet Shop Puzzle",
                    "Animal Friends Mystery",
                    "Perfect Pet Match"
                ]
            }
        }
    
    def _load_clue_templates(self) -> Dict:
        """Load templates for generating natural-sounding clues"""
        return {
            "direct_positive": [
                "The {entity} has {value}.",
                "The {entity} is {value}.",
                "{value} belongs to the {entity}."
            ],
            "direct_negative": [
                "The {entity} is not {value}.",
                "The {entity} does not have {value}.",
                "{value} does not belong to the {entity}."
            ],
            "relational": [
                "The one with {value1} is not the {entity}.",
                "The {entity1} and the one with {value} are different.",
                "If you find {value}, it's not the {entity}."
            ]
        }


def generate_puzzle_pair(child1_level: Difficulty, 
                        child2_level: Difficulty,
                        theme: Optional[str] = None) -> Tuple[LogicPuzzle, LogicPuzzle]:
    """Generate a pair of related puzzles for siblings"""
    generator = LogicPuzzleGenerator()
    
    # Use same theme for both
    if theme is None:
        theme = random.choice(list(generator.themes.keys()))
    
    # Generate collaborative base puzzle
    base_puzzle = generator.generate_puzzle(
        difficulty=child1_level,  # Use higher level as base
        theme=theme,
        collaborative=True
    )
    
    # Adapt for second child if different level
    if child1_level != child2_level:
        easier_puzzle = _adapt_puzzle_difficulty(base_puzzle, child2_level)
        return base_puzzle, easier_puzzle
    
    return base_puzzle, base_puzzle


def _adapt_puzzle_difficulty(puzzle: LogicPuzzle, 
                           target_difficulty: Difficulty) -> LogicPuzzle:
    """Adapt a puzzle to a different difficulty level"""
    # This is a simplified adaptation - in production would be more sophisticated
    if target_difficulty == Difficulty.K2:
        # Simplify clues, add visual hints
        simpler_clues = [clue.replace("does not have", "is NOT") 
                        for clue in puzzle.clues[:5]]  # Fewer clues
        
        return LogicPuzzle(
            title=puzzle.title,
            theme=puzzle.theme,
            grid_size=3,  # Smaller grid
            entities=puzzle.entities[:3],
            attributes={k: v[:3] for k, v in puzzle.attributes.items()},
            clues=simpler_clues,
            solution={e: {k: v for k, v in attrs.items()} 
                     for e, attrs in list(puzzle.solution.items())[:3]},
            difficulty=target_difficulty,
            collaborative_clues=puzzle.collaborative_clues
        )
    
    return puzzle