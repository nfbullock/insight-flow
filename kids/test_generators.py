#!/usr/bin/env python3
"""Test the content generators"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from generators.logic_puzzle_generator import LogicPuzzleGenerator, Difficulty
from generators.riddle_generator import RiddleGenerator

print("Testing Logic Puzzle Generator...")
logic_gen = LogicPuzzleGenerator()
puzzle = logic_gen.generate_puzzle(Difficulty.K2, theme="ocean")
print(f"✓ Generated {puzzle.title}")
print(f"  Grid: {puzzle.grid_size}x{puzzle.grid_size}")
print(f"  Entities: {', '.join(puzzle.entities)}")
print(f"  Clues: {len(puzzle.clues)}")

print("\nTesting Riddle Generator...")
riddle_gen = RiddleGenerator()
riddles = riddle_gen.generate_riddle_set(count=3, min_difficulty=1, max_difficulty=3)
for i, riddle in enumerate(riddles, 1):
    print(f"✓ Riddle {i}: {riddle.riddle_type.value}")
    print(f"  Q: {riddle.question[:50]}...")
    print(f"  A: {riddle.answer}")

print("\nGenerators working! ✅")