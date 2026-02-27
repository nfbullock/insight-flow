"""Math Challenge Generator for InsightFlow Kids"""

import random
from typing import Dict, List, Optional, Tuple


class MathChallengeGenerator:
    """Generate age-appropriate math challenges"""
    
    def __init__(self):
        self.problem_types = self._load_problem_types()
    
    def generate_challenge(self,
                          grade_level: float,
                          theme: str = "general",
                          visual: bool = False) -> Dict:
        """Generate math challenge appropriate for grade level"""
        
        if grade_level <= 1:  # K-1
            problem_types = ["counting", "simple_addition", "patterns", "shapes"]
        elif grade_level <= 3:  # 2-3
            problem_types = ["addition", "subtraction", "word_problems", "time", "patterns"]
        else:  # 4+
            problem_types = ["multiplication", "division", "fractions", "word_problems", "logic"]
        
        problem_type = random.choice(problem_types)
        
        generators = {
            "counting": self._generate_counting,
            "simple_addition": self._generate_simple_addition,
            "addition": self._generate_addition,
            "subtraction": self._generate_subtraction,
            "multiplication": self._generate_multiplication,
            "word_problems": self._generate_word_problem,
            "patterns": self._generate_pattern,
            "shapes": self._generate_shape_problem,
            "time": self._generate_time_problem,
            "fractions": self._generate_fraction_problem,
            "logic": self._generate_logic_problem
        }
        
        generator = generators.get(problem_type, self._generate_simple_addition)
        problem = generator(grade_level, theme)
        
        if visual:
            problem["visual_aid"] = self._add_visual_aid(problem_type, problem)
        
        return problem
    
    def _generate_counting(self, grade_level: float, theme: str) -> Dict:
        """Generate counting problems"""
        
        max_count = 20 if grade_level <= 0 else 50
        start = random.randint(0, max_count - 10)
        
        if theme == "ocean":
            objects = ["fish", "shells", "starfish", "boats"]
        elif theme == "space":
            objects = ["stars", "planets", "rockets", "aliens"]
        else:
            objects = ["apples", "books", "toys", "flowers"]
        
        obj = random.choice(objects)
        count = random.randint(start + 3, start + 10)
        
        return {
            "type": "counting",
            "problem": f"Count the {obj}. How many are there?",
            "setup": f"Start: {start} {obj}",
            "answer": count,
            "visual": f"Draw {count} {obj}"
        }
    
    def _generate_simple_addition(self, grade_level: float, theme: str) -> Dict:
        """Generate simple addition (single digit)"""
        
        a = random.randint(1, 9)
        b = random.randint(1, 9 - a)  # Keep sum under 10 for simple
        
        contexts = {
            "ocean": f"{a} fish swim by. Then {b} more join. How many fish now?",
            "space": f"{a} stars shine. {b} more appear. How many stars total?",
            "general": f"You have {a} cookies. Your friend gives you {b} more. How many do you have?"
        }
        
        return {
            "type": "addition",
            "problem": contexts.get(theme, contexts["general"]),
            "equation": f"{a} + {b} = ?",
            "answer": a + b,
            "strategy": "Count on from the bigger number"
        }
    
    def _generate_addition(self, grade_level: float, theme: str) -> Dict:
        """Generate addition problems (may include regrouping)"""
        
        if grade_level <= 2:
            a = random.randint(10, 50)
            b = random.randint(10, 50)
        else:
            a = random.randint(100, 500)
            b = random.randint(100, 500)
        
        return {
            "type": "addition",
            "problem": f"{a} + {b} = ?",
            "answer": a + b,
            "hint": "Line up the digits and add each column"
        }
    
    def _generate_subtraction(self, grade_level: float, theme: str) -> Dict:
        """Generate subtraction problems"""
        
        if grade_level <= 2:
            a = random.randint(20, 50)
            b = random.randint(5, a - 10)
        else:
            a = random.randint(100, 500)
            b = random.randint(50, a - 50)
        
        contexts = {
            "ocean": f"A ship had {a} treasures. Pirates took {b}. How many left?",
            "space": f"Mission control tracked {a} asteroids. {b} flew away. How many remain?",
            "general": f"You collected {a} stickers. You gave away {b}. How many do you still have?"
        }
        
        return {
            "type": "subtraction",
            "problem": contexts.get(theme, contexts["general"]),
            "equation": f"{a} - {b} = ?",
            "answer": a - b
        }
    
    def _generate_multiplication(self, grade_level: float, theme: str) -> Dict:
        """Generate multiplication problems"""
        
        if grade_level <= 3:
            a = random.randint(2, 5)
            b = random.randint(2, 10)
        else:
            a = random.randint(6, 12)
            b = random.randint(3, 12)
        
        contexts = {
            "ocean": f"{a} octopi each have {b} arms. How many arms total?",
            "space": f"{a} planets each have {b} moons. How many moons in all?",
            "general": f"{a} boxes each hold {b} crayons. How many crayons total?"
        }
        
        return {
            "type": "multiplication",
            "problem": contexts.get(theme, contexts["general"]),
            "equation": f"{a} × {b} = ?",
            "answer": a * b,
            "visual": f"Draw {a} groups of {b}"
        }
    
    def _generate_word_problem(self, grade_level: float, theme: str) -> Dict:
        """Generate word problems requiring multiple steps"""
        
        if grade_level <= 2:
            # Simple two-step
            a = random.randint(5, 15)
            b = random.randint(3, 10)
            c = random.randint(2, 8)
            
            problem = (f"You find {a} seashells in the morning. "
                      f"You find {b} more after lunch. "
                      f"You give {c} to your friend. How many do you keep?")
            answer = a + b - c
            steps = [f"First: {a} + {b} = {a + b}", f"Then: {a + b} - {c} = {answer}"]
        else:
            # Complex multi-step
            students = random.randint(20, 30)
            per_student = random.randint(3, 5)
            extra = random.randint(10, 20)
            
            problem = (f"A class of {students} students each brings {per_student} books. "
                      f"The teacher adds {extra} more books. "
                      f"How many books are there in total?")
            answer = (students * per_student) + extra
            steps = [f"Students bring: {students} × {per_student} = {students * per_student}",
                    f"Total: {students * per_student} + {extra} = {answer}"]
        
        return {
            "type": "word_problem",
            "problem": problem,
            "answer": answer,
            "steps": steps,
            "tip": "Break it into smaller parts!"
        }
    
    def _generate_pattern(self, grade_level: float, theme: str) -> Dict:
        """Generate number pattern problems"""
        
        if grade_level <= 1:
            # Simple counting patterns
            start = random.randint(1, 10)
            step = random.randint(1, 2)
            pattern = [start + i * step for i in range(5)]
        elif grade_level <= 3:
            # Skip counting
            start = random.randint(2, 10)
            step = random.choice([2, 5, 10])
            pattern = [start + i * step for i in range(5)]
        else:
            # Complex patterns
            if random.random() < 0.5:
                # Arithmetic sequence
                start = random.randint(3, 15)
                step = random.randint(3, 7)
                pattern = [start + i * step for i in range(5)]
            else:
                # Growing pattern
                pattern = [1, 3, 6, 10, 15]  # Triangular numbers
        
        # Hide last 1-2 numbers
        hidden = random.randint(1, 2)
        display = pattern[:-hidden]
        answers = pattern[-hidden:]
        
        return {
            "type": "pattern",
            "sequence": display + ["?"] * hidden,
            "answer": answers,
            "hint": "Look for what changes each time",
            "full_pattern": pattern
        }
    
    def _generate_shape_problem(self, grade_level: float, theme: str) -> Dict:
        """Generate geometry/shape problems"""
        
        shapes = ["triangle", "square", "rectangle", "circle", "hexagon"]
        shape = random.choice(shapes[:4] if grade_level <= 1 else shapes)
        
        if grade_level <= 1:
            # Count shapes
            count = random.randint(3, 8)
            problem = f"How many {shape}s do you see?"
            answer = count
        else:
            # Properties
            if shape == "triangle":
                problem = "How many sides does a triangle have?"
                answer = 3
            elif shape == "square":
                side = random.randint(2, 5)
                problem = f"A square has sides of {side} cm. What is its perimeter?"
                answer = side * 4
        
        return {
            "type": "shapes",
            "problem": problem,
            "shape": shape,
            "answer": answer,
            "visual": f"Draw the {shape}(s)"
        }
    
    def _generate_time_problem(self, grade_level: float, theme: str) -> Dict:
        """Generate time-based problems"""
        
        hour = random.randint(1, 12)
        minute = random.choice([0, 15, 30, 45])
        
        if grade_level <= 2:
            # Read time
            time_str = f"{hour}:{minute:02d}" if minute > 0 else f"{hour} o'clock"
            problem = f"What time does the clock show? {time_str}"
            answer = time_str
        else:
            # Elapsed time
            duration = random.choice([30, 45, 60, 90])
            problem = (f"You start reading at {hour}:{minute:02d}. "
                      f"You read for {duration} minutes. What time do you finish?")
            # Simple calculation (doesn't handle day rollover)
            end_minute = minute + duration
            end_hour = hour + end_minute // 60
            end_minute = end_minute % 60
            answer = f"{end_hour}:{end_minute:02d}"
        
        return {
            "type": "time",
            "problem": problem,
            "answer": answer,
            "visual": "Draw clock faces"
        }
    
    def _generate_fraction_problem(self, grade_level: float, theme: str) -> Dict:
        """Generate fraction problems"""
        
        if theme == "ocean":
            context = "fish in the tank"
        else:
            context = "pizza slices"
        
        total = random.choice([4, 6, 8])
        taken = random.randint(1, total - 1)
        
        problem = f"You have {total} {context}. You eat {taken}. What fraction did you eat?"
        answer = f"{taken}/{total}"
        
        return {
            "type": "fractions",
            "problem": problem,
            "answer": answer,
            "visual": f"Draw {total} parts, shade {taken}",
            "simplified": self._simplify_fraction(taken, total)
        }
    
    def _generate_logic_problem(self, grade_level: float, theme: str) -> Dict:
        """Generate mathematical logic problems"""
        
        problems = [
            {
                "setup": "Anna has 3 more marbles than Ben. Ben has 5 marbles.",
                "question": "How many marbles does Anna have?",
                "answer": 8
            },
            {
                "setup": "There are twice as many red fish as blue fish. There are 4 blue fish.",
                "question": "How many red fish are there?",
                "answer": 8
            }
        ]
        
        selected = random.choice(problems)
        
        return {
            "type": "logic",
            "problem": selected["setup"] + " " + selected["question"],
            "answer": selected["answer"],
            "strategy": "Draw a picture to help!"
        }
    
    def _add_visual_aid(self, problem_type: str, problem: Dict) -> Dict:
        """Add visual aid description"""
        
        visuals = {
            "counting": "Draw the objects in groups of 5 or 10",
            "addition": "Use base-10 blocks or draw dots",
            "subtraction": "Cross out the taken amount",
            "multiplication": "Draw equal groups",
            "pattern": "Use colors or shapes to show the pattern",
            "shapes": "Draw and label the shapes",
            "fractions": "Use pie charts or bars"
        }
        
        return {
            "description": visuals.get(problem_type, "Draw a picture to help"),
            "layout": "Leave space for drawing below the problem"
        }
    
    def _simplify_fraction(self, numerator: int, denominator: int) -> str:
        """Simplify a fraction"""
        from math import gcd
        g = gcd(numerator, denominator)
        return f"{numerator // g}/{denominator // g}"
    
    def _load_problem_types(self) -> Dict:
        """Load problem type configurations"""
        return {
            "grade_ranges": {
                "K-1": ["counting", "shapes", "patterns", "simple_addition"],
                "2-3": ["addition", "subtraction", "word_problems", "time"],
                "4-5": ["multiplication", "division", "fractions", "complex_patterns"],
                "6+": ["pre_algebra", "ratios", "percentages", "geometry"]
            }
        }