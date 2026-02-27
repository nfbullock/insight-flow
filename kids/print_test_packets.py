#!/usr/bin/env python3
"""Print test packets with ocean theme"""

import sys
import os
from pathlib import Path
from datetime import date
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))
sys.path.insert(0, str(Path(__file__).parent.parent))

from pagecraft import PDFDocument
from print_packets import create_packet_pdf, send_to_shim_printer

# Load environment
shim_env_path = Path.home() / '.openclaw/workspace-fred/.shim-env'
if shim_env_path.exists():
    with open(shim_env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"')

# Test data for both kids
test_packets = {
    'Dahlia': {
        'date': str(date.today()),
        'child_name': 'Dahlia',
        'theme': 'ocean',
        'activities': [
            {
                'type': 'morning_password',
                'content': {
                    'puzzle': '🏊 + 👍 + 🐬 = SWIM LIKE DOLPHINS',
                    'action': 'Do this together: SWIM LIKE DOLPHINS!'
                }
            },
            {
                'type': 'logic_puzzle',
                'content': {
                    'title': 'Ocean Mystery',
                    'theme': 'Creatures',
                    'entities': ['dolphin', 'octopus', 'starfish', 'seahorse'],
                    'attributes': {
                        'treasures': ['pearl', 'shell', 'coin', 'gem'],
                        'homes': ['coral reef', 'deep ocean', 'kelp forest', 'shipwreck']
                    },
                    'clues': [
                        'The dolphin does not have the pearl',
                        'The one with the shell lives in the coral reef',
                        'The octopus does not live in the deep ocean',
                        'The starfish has the coin',
                        'The creature in the kelp forest has the pearl',
                        'The seahorse lives in the shipwreck'
                    ]
                }
            },
            {
                'type': 'riddle',
                'content': {
                    'question': 'I have cities but no houses, forests but no trees, water but no fish. What am I?',
                    'hint': 'It shows places but isn\'t real'
                }
            },
            {
                'type': 'math',
                'content': {
                    'problem': 'Captain Marina\'s submarine traveled 237 meters down. Then it went 158 meters deeper. How deep is it now?',
                    'equation': '237 + 158 = ?',
                    'strategy': 'Line up the digits and add each column'
                }
            },
            {
                'type': 'creative',
                'content': {
                    'prompt': 'Draw an underwater castle',
                    'constraint': 'Use only circles and squares',
                    'extension': 'Give your castle a name and one special power!'
                }
            },
            {
                'type': 'reflection',
                'content': {
                    'prompts': [
                        'What made your brain grow today?',
                        'How did you help Xander?',
                        'What was your favorite part?'
                    ],
                    'rating': 'Circle: 😄 😐 😟',
                    'favorite': '⭐ Star your favorite activity!'
                }
            }
        ],
        'parent_notes': 'Total time: ~35 minutes. Focus on logic and collaboration.',
        'tomorrow_teaser': 'Friday fun surprises await!'
    },
    'Xander': {
        'date': str(date.today()),
        'child_name': 'Xander',
        'theme': 'ocean',
        'activities': [
            {
                'type': 'morning_password',
                'content': {
                    'puzzle': '🏊 + 👍 + 🐬 = SWIM LIKE DOLPHINS',
                    'action': 'Do this together: SWIM LIKE DOLPHINS!'
                }
            },
            {
                'type': 'logic_puzzle',
                'content': {
                    'title': 'Pet Shop by the Sea',
                    'theme': 'Animals',
                    'entities': ['fish', 'crab', 'seal'],
                    'attributes': {
                        'colors': ['blue', 'green', 'red'],
                        'toys': ['ball', 'shell', 'rock']
                    },
                    'clues': [
                        'The fish lives in the blue home',
                        'The crab is NOT green',
                        'The seal does NOT live in blue',
                        'The one with the ball is red'
                    ]
                }
            },
            {
                'type': 'riddle',
                'content': {
                    'question': 'I\'m full of holes but can hold water. What am I?',
                    'hint': 'Look in the kitchen or bathroom!'
                }
            },
            {
                'type': 'math',
                'content': {
                    'problem': 'Captain Xander saw 5 fish. Then 3 more joined. How many now?',
                    'visual': '🐠🐠🐠🐠🐠  +  🐠🐠🐠 = ?',
                    'equation': '5 + 3 = ?'
                }
            },
            {
                'type': 'creative',
                'content': {
                    'prompt': 'Draw your dream submarine',
                    'constraint': 'Make it as silly as possible!',
                    'extension': 'What special things does it have?'
                }
            },
            {
                'type': 'reflection',
                'content': {
                    'prompts': [
                        'What made your brain grow today?',
                        'What was the most fun part?',
                        'What do you want to try tomorrow?'
                    ],
                    'rating': 'Circle: 😄 😐 😟',
                    'favorite': '⭐ Star your favorite activity!'
                }
            }
        ],
        'parent_notes': 'Total time: ~30 minutes. Visual emphasis and simple logic.',
        'tomorrow_teaser': 'Friday fun surprises await!'
    }
}

# Create PDFs and send to printer
output_dir = Path(__file__).parent / "output" / "pdfs"
output_dir.mkdir(parents=True, exist_ok=True)

for child_name, packet_data in test_packets.items():
    print(f"\n📦 Processing {child_name}'s packet...")
    
    # Generate PDF
    pdf_path = output_dir / f"{child_name.lower()}-test-{date.today()}.pdf"
    create_packet_pdf(packet_data, str(pdf_path))
    
    # Send to printer
    result = send_to_shim_printer(str(pdf_path), child_name)
    
print("\n✨ Test packets sent to printer!")