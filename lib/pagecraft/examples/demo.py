#!/usr/bin/env python3
"""Generate a sample PDF that exercises every built-in module."""

import os

# Run via: make demo  (sets PYTHONPATH=lib)
from pagecraft import PDFDocument

doc = PDFDocument()

# ── Markdown ────────────────────────────────────────────────
doc.add_markdown("""
# Pagecraft Demo

This is a **demonstration** of the *Pagecraft* library.

## Features

- Modular architecture with a simple `Module` base class
- Basic **markdown** rendering (headings, lists, bold, italic, code)
- Image embedding with automatic scaling
- Logic grid puzzle generation

## How It Works

1. Create a `PDFDocument`
2. Add content with `add_markdown()`, `add_image()`, or `add_logic_grid()`
3. Call `save()` to write the PDF

---

Custom modules can be registered with `doc.register_module()` for anything
else you need — tables, charts, crosswords, you name it.
""")

doc.add_page_break()

# ── Logic Grid Puzzle ───────────────────────────────────────
doc.add_logic_grid({
    "title": "Who Lives Where?",
    "categories": {
        "People": ["Alice", "Bob", "Charlie"],
        "Houses": ["Red", "Blue", "Green"],
        "Pets":   ["Cat", "Dog", "Fish"],
    },
    "clues": [
        "Alice does not live in the red house.",
        "The person in the blue house has a cat.",
        "Bob does not have a fish.",
        "Charlie lives in the green house.",
        "The dog owner does not live in the red house.",
    ],
})

# ── Save ────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(__file__), 'demo_output.pdf')
doc.save(out)
print(f"Generated: {out}")
