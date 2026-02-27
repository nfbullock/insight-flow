"""Default styles for PDF rendering."""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor


def default_styles():
    """Build the default stylesheet used by all modules."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'MarkdownH1',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=12,
        spaceBefore=6,
    ))
    styles.add(ParagraphStyle(
        'MarkdownH2',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=10,
        spaceBefore=6,
    ))
    styles.add(ParagraphStyle(
        'MarkdownH3',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=4,
    ))
    styles.add(ParagraphStyle(
        'MarkdownH4',
        parent=styles['Heading4'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=4,
    ))
    styles.add(ParagraphStyle(
        'MarkdownBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        'MarkdownBullet',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        leftIndent=24,
        bulletIndent=12,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'PuzzleTitle',
        parent=styles['Heading2'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        'PuzzleClue',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=12,
        spaceAfter=3,
    ))

    return styles
