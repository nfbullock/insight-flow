#!/usr/bin/env python3
"""Enhanced packet generator using PageCraft properly"""

import sys
import os
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))
sys.path.insert(0, str(Path(__file__).parent.parent))

from pagecraft import PDFDocument
from print_packets import send_to_shim_printer


def create_enhanced_dahlia_packet():
    """Create Dahlia's enhanced packet"""
    
    doc = PDFDocument()
    
    # Title Page
    doc.add_markdown("""
# Dahlia's Daily Adventure

**Date:** Thursday, February 26, 2026  
**Theme:** Ocean Adventure 🌊

---

## Today's Journey - Check off as you complete!

| Morning | Afternoon | Finish Strong |
|---------|-----------|---------------|
| ☐ Password | ☐ Math | ☐ Riddle #2 |
| ☐ Logic Grid | ☐ Create | ☐ Reflection |
| ☐ Riddle #1 | ☐ Learn | ☐ Star! ⭐ |

---
""")
    
    doc.add_page_break()
    
    # Morning Password
    doc.add_markdown("""
## 🔐 Morning Password Puzzle

Work with Xander to decode today's password!

### Fill in the missing letters:

**S __ __ M** + **L __ K __** + **D __ L P H __ N S** = ?

*(swim)* + *(like)* + *(dolphins)*

---

### Write the full password here:

____________________________________

**Action:** Do this movement together!

---
""")
    
    # Logic Puzzle
    doc.add_markdown("""
## 🧩 Logic Puzzle: Ocean Mystery

Four sea creatures found different treasures in different homes.
""")
    
    categories = {
        "Creatures": ["Dolphin", "Octopus", "Starfish", "Seahorse"],
        "Treasures": ["Pearl", "Shell", "Coin", "Map"],
        "Homes": ["Coral Reef", "Deep Ocean", "Kelp Forest", "Sea Cave"]
    }
    
    clues = [
        "The dolphin does not have the pearl",
        "The creature with the shell lives in the coral reef",
        "The octopus does not live in the deep ocean",
        "The starfish found the coin",
        "The creature in the kelp forest has the pearl",
        "The seahorse explores sea caves"
    ]
    
    doc.add_logic_grid({
        "title": "",
        "categories": categories,
        "clues": clues
    })
    
    doc.add_markdown("""
💡 **TIP:** Use ✓ for YES and ✗ for NO in each box
""")
    
    doc.add_page_break()
    
    # Math Challenge
    doc.add_markdown("""
## 🔢 Math Challenge: The Deep Dive

Captain Marina's submarine made two dives today.

**First dive:** 247 meters  
**Second dive:** 186 meters deeper

**How deep is the submarine now?**

### Show your work:

```
    2 4 7
  + 1 8 6
  -------

```

**Answer:** _______ meters

---
""")
    
    # Creative Challenge
    doc.add_markdown("""
## 🎨 Creative Challenge

**Design an Underwater Castle**

Rules:
- Use ONLY circles and squares
- Give it a creative name
- Add one magical feature

### Drawing Space:

[Leave 4 inches of space here for drawing]

**Castle Name:** _________________________

**Magical Feature:** _________________________

---
""")
    
    doc.add_page_break()
    
    # Riddles
    doc.add_markdown("""
## 🤔 Riddle Time

### Riddle #1
I have cities but no houses, forests but no trees, water but no fish. What am I?

**Your answer:** _________________________

### Riddle #2 (Share with Xander!)
What has a head and a tail but no body?

**Your answer:** _________________________

---

## 💡 Did You Know?

**Dolphins have names for each other!**

Each dolphin has a unique whistle that works like a name. When they want to get a friend's attention, they copy that friend's special whistle.

**Wonder Question:** If you were a dolphin, what would your whistle sound like?

---
""")
    
    # Reflection
    doc.add_markdown("""
## 📝 Daily Reflection

### How was today's packet?

**😄 Great!** _____ **😐 OK** _____ **😟 Hard** _____

### Star Rating: ☆ ☆ ☆ ☆ ☆

### What made your brain grow today?

_________________________________________

_________________________________________

### How did you help Xander today?

_________________________________________

### Tomorrow's Adventure Awaits! 🌟
""")
    
    return doc


def create_enhanced_xander_packet():
    """Create Xander's enhanced packet with visual support"""
    
    doc = PDFDocument()
    
    # Title Page - Simple text
    doc.add_markdown("""
# Xander's Fun Day

**Date:** Thursday, February 26, 2026  
**Theme:** Ocean 🌊

---

## Check When Done!

☐ Password Game  
☐ Logic Puzzle  
☐ Riddle  
☐ Math  
☐ Draw  
☐ Learn  
☐ All Done! ⭐

---
""")
    
    doc.add_page_break()
    
    # Morning Password - Visual
    doc.add_markdown("""
## 🔐 Password Game

Work with Dahlia!

### Find the words:

**S __ __ M** = swim (like fish do)

**L __ K __** = like (I ___ pizza)

**D __ L P H __ N S** = dolphins (smart ocean animals)

### Do it: SWIM LIKE DOLPHINS!

---
""")
    
    # Logic Puzzle - Simple
    doc.add_markdown("""
## 🧩 Who Has What?

Three ocean friends have different things.
""")
    
    categories = {
        "Friends": ["Fish", "Crab", "Seal"],
        "Colors": ["Red", "Blue", "Green"],
        "Has": ["Ball", "Shell", "Star"]
    }
    
    clues = [
        "Fish is blue",
        "Crab is NOT green",
        "Red one has the ball",
        "Seal is NOT blue"
    ]
    
    doc.add_logic_grid({
        "title": "",
        "categories": categories,
        "clues": clues
    })
    
    doc.add_markdown("""
💡 Put ✓ for YES and ✗ for NO
""")
    
    doc.add_page_break()
    
    # Math - Advanced but visual
    doc.add_markdown("""
## 🔢 Math: Fish Arrays

### Look at the fish:

```
🐟 🐟 🐟 🐟 🐟 🐟
🐟 🐟 🐟 🐟 🐟 🐟
🐟 🐟 🐟 🐟 🐟 🐟
🐟 🐟 🐟 🐟 🐟 🐟
```

**Count:**
- Rows: _____
- Fish in each row: _____

**Multiply:** ____ × ____ = ____

### Now try this:

If each fish eats 3 bubbles, how many bubbles total?

____ fish × 3 bubbles = ____ bubbles

---
""")
    
    # Creative - Simple prompt
    doc.add_markdown("""
## 🎨 Draw Time

**Draw a silly submarine!**

Make it funny! Add:
☐ Big windows  
☐ Silly periscope  
☐ Funny propeller  
☐ Your idea: _______

### Draw here:

[Leave 4 inches space]

**Sub name:** _____________

---
""")
    
    doc.add_page_break()
    
    # Riddle - Simple
    doc.add_markdown("""
## 🤔 Riddle

I have lots of holes but can hold water.  
I help you clean.  
What am I?

**Hint:** Look in the kitchen!

**Circle answer:**

SPONGE    TOWEL    BRUSH

---

## 💡 Cool Fact!

**Fish can change colors!**

Some fish change color to hide.  
Like magic camouflage!

**Draw:** Color this fish to hide in rocks:

[Fish outline drawing space]

---
""")
    
    # Reflection - Visual
    doc.add_markdown("""
## 📝 How Was Today?

### Circle one:

# 😄    😐    😟

### Best part (draw or write):

[Space for drawing]

### Stars: ☆ ☆ ☆ ☆ ☆

Great job! See you tomorrow! 🌟
""")
    
    return doc


# Main execution
if __name__ == "__main__":
    # Load environment
    shim_env_path = Path.home() / '.openclaw/workspace-fred/.shim-env'
    if shim_env_path.exists():
        with open(shim_env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
    
    print("🎨 Creating enhanced packets...")
    
    output_dir = Path(__file__).parent / "output" / "enhanced"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate Dahlia's packet
    dahlia_doc = create_enhanced_dahlia_packet()
    dahlia_path = output_dir / f"dahlia-enhanced-{date.today()}.pdf"
    dahlia_doc.save(str(dahlia_path))
    print(f"✓ Created Dahlia's packet: {dahlia_path}")
    
    # Generate Xander's packet
    xander_doc = create_enhanced_xander_packet()
    xander_path = output_dir / f"xander-enhanced-{date.today()}.pdf"
    xander_doc.save(str(xander_path))
    print(f"✓ Created Xander's packet: {xander_path}")
    
    # Send to printer
    print("\n📤 Sending to printer...")
    send_to_shim_printer(str(dahlia_path), "Dahlia")
    send_to_shim_printer(str(xander_path), "Xander")
    
    print("\n✨ Enhanced packets sent!")