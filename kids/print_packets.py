#!/usr/bin/env python3
"""Generate and print daily packets via shim API"""

import sys
import os
import json
import requests
from datetime import date
from pathlib import Path

# Add lib to path for PageCraft
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))
sys.path.insert(0, str(Path(__file__).parent.parent))

from pagecraft import PDFDocument
from generators.daily_packet_generator import DailyPacketGenerator
from generators.logic_puzzle_generator import Difficulty
from generators.riddle_generator import generate_daily_riddles


def create_packet_pdf(packet_data, output_path):
    """Convert packet data to PDF using PageCraft"""
    
    doc = PDFDocument()
    
    # Title page
    doc.add_markdown(f"""
# {packet_data['child_name']}'s Daily Adventure

**Date:** {packet_data['date']}  
**Theme:** {packet_data['theme'].title()} 🌊

---

## Morning Password

Work together to unlock today's fun!
""")
    
    # Add activities
    for i, activity in enumerate(packet_data['activities'], 1):
        activity_type = activity['type']
        content = activity['content']
        
        if activity_type == 'morning_password':
            doc.add_markdown(f"""
### 🔐 Decode the Password

**Puzzle:** {content['puzzle']}

**Action:** {content['action']}

---
""")
        
        elif activity_type == 'logic_puzzle':
            # Add logic grid
            categories = {}
            # First category is entities (rows)
            categories[content['theme'].title()] = content['entities']
            # Add attribute categories
            for attr_name, attr_values in content['attributes'].items():
                categories[attr_name.title()] = attr_values
            
            doc.add_markdown(f"## 🧩 Logic Puzzle: {content['title']}")
            doc.add_logic_grid({
                "title": content['title'],
                "categories": categories,
                "clues": content['clues']
            })
            
        elif activity_type == 'riddle':
            doc.add_markdown(f"""
## 🤔 Riddle Time

{content['question']}

*Hint: {content.get('hint', 'Think carefully!')}*

---
""")
        
        elif activity_type == 'creative':
            doc.add_markdown(f"""
## 🎨 Creative Challenge

**{content.get('prompt', 'Create something amazing!')}**

{content.get('constraint', '')}

{content.get('extension', '')}

---
""")
        
        elif activity_type == 'math':
            doc.add_markdown(f"""
## 🔢 Math Challenge

**{content.get('problem', 'Solve this problem')}**

{content.get('equation', '')}

{content.get('visual', '')}

*{content.get('strategy', 'Think step by step')}*

---
""")
        
        elif activity_type == 'knowledge':
            doc.add_markdown(f"""
## 💡 Did You Know?

**{content.get('fact', 'Amazing fact!')}**

{content.get('explanation', '')}

{content.get('wonder_prompt', 'What do you wonder about this?')}

---
""")
        
        elif activity_type == 'reflection':
            prompts_text = '\n'.join([f"{i}. {p}" for i, p in enumerate(content['prompts'], 1)])
            doc.add_markdown(f"""
## 📝 Daily Reflection

{prompts_text}

{content.get('rating', '')}

{content.get('favorite', '')}

---
""")
    
    # Add footer
    doc.add_markdown(f"""
---

**{packet_data.get('parent_notes', '')}**

**Coming Tomorrow:** {packet_data.get('tomorrow_teaser', 'More adventures await!')}
""")
    
    # Save PDF
    doc.save(output_path)
    print(f"✓ Created PDF: {output_path}")
    return output_path


def send_to_shim_printer(pdf_path, child_name):
    """Send PDF to shim print API"""
    
    # Load auth token
    token = os.environ.get('SHIM_AUTH_TOKEN')
    if not token:
        raise ValueError("SHIM_AUTH_TOKEN not found in environment")
    
    shim_url = "https://shim.bullock.im/print"
    
    with open(pdf_path, 'rb') as f:
        files = {'file': (f'InsightFlow-{child_name}-{date.today()}.pdf', f, 'application/pdf')}
        headers = {'Authorization': f'Bearer {token}'}
        
        print(f"📤 Sending {child_name}'s packet to printer...")
        response = requests.post(shim_url, files=files, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Print job submitted: {result}")
            return result
        else:
            print(f"❌ Print failed: {response.status_code} - {response.text}")
            return None


def main():
    """Generate and print today's packets"""
    
    # Load environment
    shim_env_path = Path.home() / '.openclaw/workspace-fred/.shim-env'
    if shim_env_path.exists():
        with open(shim_env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
    
    print("🌟 InsightFlow Kids - Daily Packet Printer")
    print(f"📅 Date: {date.today()}")
    
    # Generate packets
    generator = DailyPacketGenerator()
    packets = generator.generate_daily_packets()
    
    # Create output directory
    output_dir = Path(__file__).parent / "output" / "pdfs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each child's packet
    for child_name, packet in packets.items():
        print(f"\n📦 Processing {child_name}'s packet...")
        
        # Convert to dict for PDF generation
        packet_dict = {
            'date': packet.date,
            'child_name': packet.child_name,
            'theme': packet.theme,
            'activities': packet.activities,
            'parent_notes': packet.parent_notes,
            'tomorrow_teaser': packet.tomorrow_teaser
        }
        
        # Generate PDF
        pdf_path = output_dir / f"{child_name.lower()}-{date.today()}.pdf"
        create_packet_pdf(packet_dict, str(pdf_path))
        
        # Send to printer
        send_to_shim_printer(str(pdf_path), child_name)
    
    print("\n✨ Daily packets complete!")


if __name__ == "__main__":
    main()