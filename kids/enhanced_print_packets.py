#!/usr/bin/env python3
"""Enhanced packet generator with visual improvements"""

import sys
import os
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))
sys.path.insert(0, str(Path(__file__).parent.parent))

from pagecraft import PDFDocument
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus.flowables import HRFlowable
from print_packets import send_to_shim_printer


def create_enhanced_packet(child_name, is_advanced_reader=True):
    """Create visually enhanced packet with proper formatting"""
    
    doc = PDFDocument()
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#A23B72'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    # Title Page with border
    doc.story.append(Paragraph(f"{child_name}'s Daily Adventure", title_style))
    doc.story.append(Paragraph(f"Date: {date.today().strftime('%A, %B %d, %Y')}", styles['Normal']))
    doc.story.append(Spacer(1, 0.5*inch))
    
    # Progress Tracker
    progress_data = [
        ['☐ Morning Password', '☐ Logic Puzzle', '☐ Riddle #1'],
        ['☐ Math Challenge', '☐ Creative Time', '☐ Did You Know?'],
        ['☐ Riddle #2', '☐ Reflection', '☐ All Done! ⭐']
    ]
    
    progress_table = Table(progress_data, colWidths=[2*inch, 2*inch, 2*inch])
    progress_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA'))
    ]))
    
    doc.story.append(Paragraph("Today's Activities - Check off as you go!", section_style))
    doc.story.append(progress_table)
    doc.story.append(PageBreak())
    
    # Morning Password - Visual Version
    doc.story.append(Paragraph("🔐 Morning Password Puzzle", section_style))
    
    password_data = [
        ['S _ _ M', '+', 'L _ K _', '+', 'D _ L P H _ N S', '=', '?'],
        ['(swim)', '', '(like)', '', '(dolphins)', '', '']
    ]
    
    password_table = Table(password_data)
    password_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 16),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.grey)
    ]))
    
    doc.story.append(password_table)
    doc.story.append(Spacer(1, 0.3*inch))
    
    # Answer box with dotted lines
    answer_box_data = [['Write the password here: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _']]
    answer_table = Table(answer_box_data, colWidths=[6*inch])
    answer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20)
    ]))
    
    doc.story.append(answer_table)
    doc.story.append(Paragraph("Action: Do this together with your sibling!", styles['Italic']))
    doc.story.append(HRFlowable(width="80%", thickness=1, color=colors.grey))
    doc.story.append(Spacer(1, 0.5*inch))
    
    # Logic Puzzle with Visual Grid
    doc.story.append(Paragraph("🧩 Logic Puzzle: Ocean Mystery", section_style))
    
    if child_name == "Dahlia":
        # Advanced version
        categories = {
            "Creatures": ["Dolphin", "Octopus", "Starfish", "Seahorse"],
            "Treasures": ["Pearl", "Shell", "Coin", "Map"],
            "Homes": ["Reef", "Deep Sea", "Kelp", "Cave"]
        }
        clues = [
            "1. The dolphin does not have the pearl",
            "2. The one with the shell lives in the reef",
            "3. The octopus is not in the deep sea",
            "4. The starfish found the coin",
            "5. The kelp forest hides the pearl",
            "6. The seahorse explores caves"
        ]
    else:
        # Simplified for Xander with visual support
        categories = {
            "Animals": ["Fish 🐠", "Crab 🦀", "Seal 🦭"],
            "Colors": ["Red", "Blue", "Green"],
            "Toys": ["Ball ⚪", "Shell 🐚", "Star ⭐"]
        }
        clues = [
            "1. Fish = Blue (The fish is blue)",
            "2. Crab ≠ Green (Crab is NOT green)",  
            "3. Red = Ball (Red one has the ball)",
            "4. Seal ≠ Blue (Seal is NOT blue)"
        ]
    
    doc.add_logic_grid({
        "title": "",
        "categories": categories,
        "clues": clues
    })
    
    # Visual tip box
    tip_data = [['💡 TIP: Use ✓ for YES and ✗ for NO in each box']]
    tip_table = Table(tip_data, colWidths=[5*inch])
    tip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF3CD')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
    ]))
    doc.story.append(Spacer(1, 0.2*inch))
    doc.story.append(tip_table)
    doc.story.append(PageBreak())
    
    # Math Challenge - Visual for Xander
    doc.story.append(Paragraph("🔢 Math Challenge", section_style))
    
    if child_name == "Xander":
        # Advanced math with visual support
        doc.story.append(Paragraph("Array Multiplication", styles['Normal']))
        
        # Visual array
        array_data = []
        for i in range(4):
            row = ['🐟'] * 6
            array_data.append(row)
        
        array_table = Table(array_data)
        array_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 20)
        ]))
        
        doc.story.append(array_table)
        doc.story.append(Spacer(1, 0.2*inch))
        
        math_text = """
        Count: ____ rows × ____ fish in each row = ____ total fish
        
        Write as multiplication: ____ × ____ = ____
        """
        doc.story.append(Paragraph(math_text, styles['Normal']))
    else:
        # Dahlia's version with word problem
        doc.story.append(Paragraph("The Deep Dive", styles['Normal']))
        doc.story.append(Paragraph(
            "Captain Marina dove 247 meters. Then 186 meters more. How deep?",
            styles['Normal']
        ))
        
        # Visual workspace
        workspace_data = [
            ['', '2', '4', '7'],
            ['+', '1', '8', '6'],
            ['', '―', '―', '―'],
            ['', '_', '_', '_']
        ]
        
        workspace_table = Table(workspace_data, colWidths=[0.5*inch]*4)
        workspace_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 18),
            ('GRID', (1, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        doc.story.append(workspace_table)
    
    doc.story.append(HRFlowable(width="80%", thickness=1, color=colors.grey))
    doc.story.append(PageBreak())
    
    # Creative Section with Drawing Box
    doc.story.append(Paragraph("🎨 Creative Challenge", section_style))
    
    if child_name == "Xander":
        doc.story.append(Paragraph("Draw: Silly Sub", styles['Normal']))
        doc.story.append(Paragraph("Make it funny! Add:", styles['Normal']))
        doc.story.append(Paragraph("☐ Windows  ☐ Propeller  ☐ Periscope  ☐ Your idea: ____", 
                                 styles['Normal']))
    else:
        doc.story.append(Paragraph("Design an Underwater Castle", styles['Normal']))
        doc.story.append(Paragraph("Rule: Only use circles and squares!", styles['Normal']))
    
    # Drawing box
    drawing_box = Table([['', '', ''], ['', 'Draw Here!', ''], ['', '', '']], 
                       colWidths=[2*inch, 2*inch, 2*inch],
                       rowHeights=[1.5*inch, 1.5*inch, 1.5*inch])
    drawing_box.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 2, colors.grey),
        ('ALIGN', (1, 1), (1, 1), 'CENTER'),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.lightgrey),
        ('FONTSIZE', (1, 1), (1, 1), 24)
    ]))
    
    doc.story.append(drawing_box)
    doc.story.append(PageBreak())
    
    # Reflection with emotion faces
    doc.story.append(Paragraph("📝 Daily Reflection", section_style))
    
    reflection_data = [
        ['How was today?', '😄', '😐', '😟'],
        ['Circle one:', 'Great!', 'OK', 'Hard']
    ]
    
    reflection_table = Table(reflection_data)
    reflection_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (1, 0), (3, 0), 24),
        ('FONTSIZE', (0, 0), (0, -1), 12),
        ('FONTSIZE', (1, 1), (3, 1), 10)
    ]))
    
    doc.story.append(reflection_table)
    doc.story.append(Spacer(1, 0.3*inch))
    
    # Star rating
    star_data = [['Star your favorite:', '☆', '☆', '☆', '☆', '☆']]
    star_table = Table(star_data)
    star_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (1, 0), (-1, 0), 20)
    ]))
    
    doc.story.append(star_table)
    doc.story.append(Spacer(1, 0.3*inch))
    
    # Learning prompt with lines
    if child_name == "Xander":
        doc.story.append(Paragraph("Draw one thing you learned:", styles['Normal']))
        doc.story.append(drawing_box)  # Reuse drawing box
    else:
        doc.story.append(Paragraph("What made your brain grow today?", styles['Normal']))
        doc.story.append(Paragraph("_" * 60, styles['Normal']))
        doc.story.append(Paragraph("_" * 60, styles['Normal']))
    
    # Footer
    doc.story.append(HRFlowable(width="100%", thickness=2, color=colors.black))
    doc.story.append(Paragraph("Great job today! See you tomorrow! 🌟", 
                             ParagraphStyle('Footer', 
                                          parent=styles['Normal'],
                                          alignment=TA_CENTER,
                                          fontSize=14,
                                          textColor=colors.HexColor('#2E86AB'))))
    
    # Save
    output_dir = Path(__file__).parent / "output" / "enhanced"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f"{child_name.lower()}-enhanced-{date.today()}.pdf"
    doc.save(str(pdf_path))
    
    return str(pdf_path)


# Generate enhanced packets
print("🎨 Creating enhanced packets with visual improvements...")

dahlia_pdf = create_enhanced_packet("Dahlia", is_advanced_reader=True)
print(f"✓ Created Dahlia's enhanced packet: {dahlia_pdf}")

xander_pdf = create_enhanced_packet("Xander", is_advanced_reader=False)
print(f"✓ Created Xander's enhanced packet: {xander_pdf}")

# Send to printer
print("\n📤 Sending to printer...")
send_to_shim_printer(dahlia_pdf, "Dahlia")
send_to_shim_printer(xander_pdf, "Xander")

print("\n✨ Enhanced packets sent!")