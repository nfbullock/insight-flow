"""Core PDFDocument class for building and rendering PDF documents."""

import io

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak

from .styles import default_styles
from .modules import ModuleRegistry


class PDFDocument:
    """A hackable PDF document builder.

    Usage:
        doc = PDFDocument()
        doc.add_markdown("# Hello\\nSome text")
        doc.add_image("photo.png")
        doc.add_logic_grid({...})
        doc.save("output.pdf")
    """

    def __init__(self, pagesize=LETTER, margins=None):
        self.pagesize = pagesize
        self.margins = margins or {
            'top': 0.75 * inch,
            'bottom': 0.75 * inch,
            'left': 0.75 * inch,
            'right': 0.75 * inch,
        }
        self.styles = default_styles()
        self.content = []  # list of reportlab flowables
        self._registry = ModuleRegistry()
        self._register_builtins()

    def _register_builtins(self):
        from .modules.markdown import MarkdownModule
        from .modules.image import ImageModule
        from .modules.logic_grid import LogicGridModule

        self._registry.register('markdown', MarkdownModule())
        self._registry.register('image', ImageModule())
        self._registry.register('logic_grid', LogicGridModule())

    def register_module(self, name, module):
        """Register a custom module."""
        self._registry.register(name, module)

    def add(self, module_name, data, **kwargs):
        """Add content using a named module."""
        module = self._registry.get(module_name)
        flowables = module.render(data, self.styles, self.pagesize, **kwargs)
        self.content.extend(flowables)

    def add_markdown(self, text, **kwargs):
        """Add markdown-formatted text."""
        self.add('markdown', text, **kwargs)

    def add_image(self, path, **kwargs):
        """Add an image from a file path."""
        self.add('image', path, **kwargs)

    def add_logic_grid(self, puzzle_dict, **kwargs):
        """Add a logic grid puzzle from a dictionary."""
        self.add('logic_grid', puzzle_dict, **kwargs)

    def add_spacer(self, height=0.25 * inch):
        """Add vertical whitespace."""
        self.content.append(Spacer(1, height))

    def add_page_break(self):
        """Force a new page."""
        self.content.append(PageBreak())

    def add_flowable(self, flowable):
        """Add a raw reportlab flowable directly."""
        self.content.append(flowable)

    def save(self, filename):
        """Write the PDF to a file."""
        doc = SimpleDocTemplate(
            filename,
            pagesize=self.pagesize,
            topMargin=self.margins['top'],
            bottomMargin=self.margins['bottom'],
            leftMargin=self.margins['left'],
            rightMargin=self.margins['right'],
        )
        doc.build(self.content)

    def save_bytes(self):
        """Return the PDF as bytes (useful for web responses)."""
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=self.pagesize,
            topMargin=self.margins['top'],
            bottomMargin=self.margins['bottom'],
            leftMargin=self.margins['left'],
            rightMargin=self.margins['right'],
        )
        doc.build(self.content)
        return buf.getvalue()
