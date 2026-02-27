"""Pagecraft - A hackable, modular PDF generation library.

Usage:
    from pagecraft import PDFDocument

    doc = PDFDocument()
    doc.add_markdown("# Hello\\nSome **bold** text.")
    doc.add_image("photo.png")
    doc.add_logic_grid({"title": "...", "categories": {...}, "clues": [...]})
    doc.save("output.pdf")
"""

from .document import PDFDocument
from .modules import Module

__all__ = ["PDFDocument", "Module"]
__version__ = "0.1.0"
