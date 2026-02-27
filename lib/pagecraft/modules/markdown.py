"""Markdown to PDF rendering module.

Supports: headings (h1-h4), **bold**, *italic*, `code`,
bullet lists, numbered lists, horizontal rules, and paragraphs.
"""

import re

from . import Module
from reportlab.platypus import Paragraph, Spacer, HRFlowable
from reportlab.lib.colors import HexColor


def _inline_format(text):
    """Convert markdown inline formatting to reportlab XML markup."""
    # Escape XML entities first
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')

    # Inline code (handle first to protect contents from further parsing)
    text = re.sub(r'`([^`]+)`', r'<font face="Courier">\1</font>', text)

    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Italic
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)

    return text


def _parse_blocks(text):
    """Parse markdown text into a list of typed blocks."""
    lines = text.split('\n')
    blocks = []
    current = None

    def flush():
        nonlocal current
        if current:
            blocks.append(current)
            current = None

    for line in lines:
        stripped = line.strip()

        # Blank line ends the current block
        if not stripped:
            flush()
            continue

        # Heading
        m = re.match(r'^(#{1,4})\s+(.+)$', stripped)
        if m:
            flush()
            blocks.append({
                'type': 'heading',
                'level': len(m.group(1)),
                'text': m.group(2),
            })
            continue

        # Horizontal rule
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            flush()
            blocks.append({'type': 'hr'})
            continue

        # Bullet list item
        m = re.match(r'^[-*+]\s+(.+)$', stripped)
        if m:
            if current and current['type'] != 'bullet_list':
                flush()
            if not current:
                current = {'type': 'bullet_list', 'items': []}
            current['items'].append(m.group(1))
            continue

        # Numbered list item
        m = re.match(r'^\d+\.\s+(.+)$', stripped)
        if m:
            if current and current['type'] != 'numbered_list':
                flush()
            if not current:
                current = {'type': 'numbered_list', 'items': []}
            current['items'].append(m.group(1))
            continue

        # Regular paragraph text
        if current and current['type'] == 'paragraph':
            current['text'] += ' ' + stripped
        else:
            flush()
            current = {'type': 'paragraph', 'text': stripped}

    flush()
    return blocks


_HEADING_STYLES = {
    1: 'MarkdownH1',
    2: 'MarkdownH2',
    3: 'MarkdownH3',
    4: 'MarkdownH4',
}


class MarkdownModule(Module):
    """Renders basic markdown text into PDF flowables."""

    def render(self, data, styles, pagesize, **kwargs):
        blocks = _parse_blocks(data)
        flowables = []

        for block in blocks:
            btype = block['type']

            if btype == 'heading':
                style_name = _HEADING_STYLES.get(block['level'], 'MarkdownH4')
                text = _inline_format(block['text'])
                flowables.append(Paragraph(text, styles[style_name]))

            elif btype == 'paragraph':
                text = _inline_format(block['text'])
                flowables.append(Paragraph(text, styles['MarkdownBody']))

            elif btype == 'bullet_list':
                for item in block['items']:
                    text = _inline_format(item)
                    flowables.append(Paragraph(
                        f'\u2022  {text}', styles['MarkdownBullet']
                    ))

            elif btype == 'numbered_list':
                for i, item in enumerate(block['items'], 1):
                    text = _inline_format(item)
                    flowables.append(Paragraph(
                        f'{i}.  {text}', styles['MarkdownBullet']
                    ))

            elif btype == 'hr':
                flowables.append(Spacer(1, 6))
                flowables.append(HRFlowable(
                    width="100%",
                    thickness=1,
                    color=HexColor('#CCCCCC'),
                    spaceAfter=6,
                ))

        return flowables
