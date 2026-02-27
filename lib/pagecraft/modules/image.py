"""Image embedding module."""

import os

from . import Module
from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor


class ImageModule(Module):
    """Embeds an image into the PDF.

    Keyword args:
        width:     Explicit width in points.
        height:    Explicit height in points.
        max_width: Maximum width before scaling (defaults to usable page width).
        caption:   Optional caption string below the image.
    """

    def render(self, data, styles, pagesize, **kwargs):
        path = data
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image not found: {path}")

        width = kwargs.get('width')
        height = kwargs.get('height')
        max_width = kwargs.get('max_width')
        caption = kwargs.get('caption')

        usable_width = max_width or (pagesize[0] - 1.5 * inch)

        img = Image(path)

        if width and height:
            img.drawWidth = width
            img.drawHeight = height
        elif width:
            aspect = img.imageHeight / img.imageWidth
            img.drawWidth = width
            img.drawHeight = width * aspect
        elif height:
            aspect = img.imageWidth / img.imageHeight
            img.drawHeight = height
            img.drawWidth = height * aspect
        else:
            # Scale down to fit if necessary
            if img.imageWidth > usable_width:
                aspect = img.imageHeight / img.imageWidth
                img.drawWidth = usable_width
                img.drawHeight = usable_width * aspect

        flowables = [img]

        if caption:
            cap_style = ParagraphStyle(
                'ImageCaption',
                parent=styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                spaceAfter=8,
                textColor=HexColor('#666666'),
            )
            flowables.append(Paragraph(caption, cap_style))

        return flowables
