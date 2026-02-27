#!/usr/bin/env python3
"""Test PDF generation with sample data"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))

from pagecraft import PDFDocument
import json

# Load test data
dahlia_data = {
    'date': '2026-02-26',
    'child_name': 'Dahlia',
    'theme': 'ocean',
    'activities': [
        {
            'type': 'morning_password',
            'content': {
                'puzzle': '🏊 + 👍 + 🐬 = ?',
                'answer': 'SWIM LIKE DOLPHINS',
                'action': 'Do this together: SWIM LIKE DOLPHINS!'
            }
        },
        {
            'type': 'logic_puzzle',
            'content': {
                'title': 'Ocean Mystery',
                'theme': 'Ocean Creatures',
                'entities': ['dolphin', 'octopus', 'starfish'],
                'attributes': {
                    'treasures': ['pearl', 'shell', 'coin'],
                    'homes': ['coral reef', 'deep ocean', 'kelp forest']
                },
                'clues': [
                    'The dolphin does not have the pearl',
                    'The one with the shell lives in the coral reef',
                    'The octopus does not live in the deep ocean',
                    'The starfish has the coin',
                    'The creature in the kelp forest has the pearl'
                ]
            }
        }
    ],
    'parent_notes': 'Total time: ~35 minutes',
    'tomorrow_teaser': 'Friday fun surprises await!'
}

# Create simple PDF
doc = PDFDocument()

doc.add_markdown(f"""
# {dahlia_data['child_name']}'s Daily Adventure

**Date:** {dahlia_data['date']}  
**Theme:** Ocean 🌊

## Morning Password

Work with Xander to decode: {dahlia_data['activities'][0]['content']['puzzle']}
""")

# Add logic grid
puzzle = dahlia_data['activities'][1]['content']
categories = {
    'Creatures': puzzle['entities'],
    'Treasures': puzzle['attributes']['treasures'],
    'Homes': puzzle['attributes']['homes']
}

doc.add_logic_grid({
    'title': puzzle['title'],
    'categories': categories,
    'clues': puzzle['clues']
})

# Save
output_path = Path(__file__).parent / 'test_dahlia.pdf'
doc.save(str(output_path))
print(f"✓ Created test PDF: {output_path}")