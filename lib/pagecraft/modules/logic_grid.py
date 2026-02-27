"""Logic grid puzzle module.

Draws the standard L-shaped logic grid used in deduction puzzles,
with rotated column headers and category labels.

Expected input format:
    {
        "title": "Who Lives Where?",
        "categories": {
            "People": ["Alice", "Bob", "Charlie"],
            "Colors": ["Red", "Blue", "Green"],
            "Pets":   ["Cat", "Dog", "Fish"],
        },
        "clues": [
            "Alice does not live in the red house.",
            "The person in the blue house has a cat.",
        ]
    }

Category order matters: the first category becomes the row labels at the
top of the grid; the rest become column headers.  Additional row groups
are added below in reverse order to form the standard staircase shape.
"""

import math

from . import Module
from reportlab.platypus import Flowable, Paragraph, Spacer
from reportlab.lib.colors import black


class LogicGridFlowable(Flowable):
    """Custom flowable that draws an L-shaped logic grid."""

    def __init__(self, categories, cell_size=18):
        Flowable.__init__(self)
        self.categories = categories  # list of (name, [items])
        self.cs = cell_size

        self.n = len(categories)
        self.m = len(categories[0][1])
        for name, items in categories:
            if len(items) != self.m:
                raise ValueError(
                    f"All categories need the same item count. "
                    f"'{name}' has {len(items)}, expected {self.m}."
                )

        # Column groups (across the top): categories[1:]
        self.col_groups = list(categories[1:])

        # Row groups (down the left): categories[0], then categories[-1 .. 2]
        self.row_groups = [categories[0]]
        if self.n > 2:
            self.row_groups += list(reversed(categories[2:]))

        # Number of column groups each row group uses
        # Row 0 uses all; row k (k>=1) uses n-1-k
        self.row_col_counts = [len(self.col_groups)]
        for k in range(1, len(self.row_groups)):
            self.row_col_counts.append(len(self.col_groups) - k)

        # Layout constants
        self.cat_label_w = 18     # width for vertical category name
        self.cat_header_h = 14    # height for column category name
        self.group_gap = 3        # gap between grid sections
        self.rotate_deg = 55
        self.label_font_size = 7

        # Calculate row label width from the longest row item
        all_row_items = [it for _, items in self.row_groups for it in items]
        longest_row = max(len(s) for s in all_row_items) if all_row_items else 3
        self.label_w = longest_row * (self.label_font_size * 0.6) + 10

        # Calculate header height from the longest column label
        all_col_items = [it for _, items in self.col_groups for it in items]
        longest_col = max(len(s) for s in all_col_items) if all_col_items else 3
        text_w = longest_col * 4.5  # approximate width at font size 7
        rad = math.radians(self.rotate_deg)
        self.header_h = text_w * math.sin(rad) + 8  # +padding

        # Compute total dimensions
        max_col_groups = len(self.col_groups)
        total_grid_cols = max_col_groups * self.m
        total_grid_rows = len(self.row_groups) * self.m

        self.total_w = (self.cat_label_w + self.label_w
                        + total_grid_cols * self.cs
                        + (max_col_groups - 1) * self.group_gap)
        self.total_h = (self.cat_header_h + self.header_h
                        + total_grid_rows * self.cs
                        + (len(self.row_groups) - 1) * self.group_gap)

    def wrap(self, availWidth, availHeight):
        return (self.total_w, self.total_h)

    def draw(self):
        c = self.canv
        cs = self.cs

        # Grid origin: top-left corner of the cell area
        gx0 = self.cat_label_w + self.label_w
        gy0 = self.total_h - self.cat_header_h - self.header_h

        # ── Column headers ──────────────────────────────────────
        x_off = gx0
        for cat_name, items in self.col_groups:
            # Category name centered above its columns
            cx = x_off + (self.m * cs) / 2
            cy = self.total_h - self.cat_header_h / 2
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(cx, cy - 3, cat_name)

            # Item names rotated 45°
            c.setFont("Helvetica", 7)
            for i, item in enumerate(items):
                ix = x_off + i * cs + cs * 0.4
                iy = gy0 + 2
                c.saveState()
                c.translate(ix, iy)
                c.rotate(55)
                c.drawString(0, 0, item)
                c.restoreState()

            x_off += self.m * cs + self.group_gap

        # ── Row groups ──────────────────────────────────────────
        y_off = gy0
        for ri, (row_cat, row_items) in enumerate(self.row_groups):
            ncols = self.row_col_counts[ri]

            # Vertical category label
            cy = y_off - (self.m * cs) / 2
            c.saveState()
            c.setFont("Helvetica-Bold", 8)
            c.translate(self.cat_label_w / 2, cy)
            c.rotate(90)
            c.drawCentredString(0, -3, row_cat)
            c.restoreState()

            # Row item labels
            c.setFont("Helvetica", 7)
            for j, item in enumerate(row_items):
                iy = y_off - j * cs - cs / 2
                c.drawRightString(
                    self.cat_label_w + self.label_w - 4, iy - 2, item
                )

            # Grid cells for each column group this row uses
            x_off = gx0
            for ci in range(ncols):
                # Individual cells
                c.setStrokeColor(black)
                c.setLineWidth(0.4)
                for row in range(self.m):
                    for col in range(self.m):
                        cx = x_off + col * cs
                        cy_cell = y_off - (row + 1) * cs
                        c.rect(cx, cy_cell, cs, cs, stroke=1, fill=0)

                # Thick border around the section
                c.setLineWidth(1.5)
                c.rect(x_off, y_off - self.m * cs,
                       self.m * cs, self.m * cs, stroke=1, fill=0)

                x_off += self.m * cs + self.group_gap

            y_off -= self.m * cs + self.group_gap

        c.setLineWidth(1)


class LogicGridModule(Module):
    """Renders a logic grid puzzle from a dictionary."""

    def render(self, data, styles, pagesize, **kwargs):
        flowables = []
        cell_size = kwargs.get('cell_size', 18)

        # Title
        title = data.get('title', 'Logic Grid Puzzle')
        flowables.append(Paragraph(title, styles['PuzzleTitle']))

        # Grid
        categories = list(data['categories'].items())
        if len(categories) < 2:
            raise ValueError("A logic grid requires at least 2 categories.")
        grid = LogicGridFlowable(categories, cell_size=cell_size)
        flowables.append(grid)
        flowables.append(Spacer(1, 14))

        # Clues
        clues = data.get('clues', [])
        if clues:
            flowables.append(Paragraph("Clues:", styles['MarkdownH3']))
            for i, clue in enumerate(clues, 1):
                flowables.append(Paragraph(
                    f"{i}. {clue}", styles['PuzzleClue']
                ))

        return flowables
