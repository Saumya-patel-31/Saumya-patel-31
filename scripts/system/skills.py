"""The Skills window: languages, infra and tools as glowing glyph tiles."""

from . import content as c
from .icons import GLYPHS
from .theme import HOLO, ICE, MUTED, VIOLET, chip, delay, divider, document, text, window

# Simple Icons dropped AWS, so this is a plain "aws" wordmark with a smile arrow.
AWS_GLYPH = (
    text(12, 13, "aws", size=10.5, color=ICE, cls="sans", anchor="middle", weight=800)
    + f'<path d="M4.5 16.6c4.6 2.9 10.4 2.9 15 0M17 15.2l2.7 1.3-1.2 2.7" fill="none" stroke="{ICE}" '
    f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
)

TILE, PITCH, TILES_X, ROW_H = 52, 66, 236, 104


def _glyph(key):
    if key == "aws":
        return AWS_GLYPH
    return f'<path d="{GLYPHS[key]}" fill="{ICE}" fill-opacity=".92"/>'


def render_skills():
    w, h = 884, 424
    parts = []
    n = 0
    for row, group in enumerate(c.SKILLS):
        top = 66 + row * ROW_H
        if row:
            parts.append(divider(28, w - 28, top - 14, opacity=0.1))
        parts.append(text(36, top + 24, group.name, size=13, color=HOLO, cls="sans", weight=700, spacing=2.5))
        parts.append(text(36, top + 42, group.caption, size=11, color=MUTED))
        for i, skill in enumerate(group.skills):
            x = TILES_X + i * PITCH
            parts.append(
                f'<g class="fade" {delay(0.2 + n * 0.04)}>'
                f'<rect x="{x}" y="{top}" width="{TILE}" height="{TILE}" rx="9" fill="#0d2140" '
                f'stroke="{HOLO}" stroke-opacity=".35"/>'
                f'<g transform="translate({x + 14} {top + 14})" filter="url(#glow)">{_glyph(skill.glyph)}</g>'
                + text(x + TILE / 2, top + TILE + 16, skill.label, size=10, color=MUTED, anchor="middle")
                + "</g>"
            )
            n += 1
    parts.append(divider(28, w - 28, 352, opacity=0.1))
    parts.append(text(36, 391, "ACQUIRED TITLE", size=11, color=MUTED, spacing=1.5))
    title_chip, _ = chip(170, 392, c.CERT, color=VIOLET, fill_opacity=0.18, size=12, spacing=1, text_color=ICE)
    parts.append(f'<g filter="url(#glow)">{title_chip}</g>')

    win, css = window(8, 8, w, h, title="SKILLS", uid="sk", body="".join(parts))
    names = "; ".join(f"{g.name.title()}: " + ", ".join(s.label for s in g.skills) for g in c.SKILLS)
    return document(w + 16, h + 16, win, title=f"Skills. {names}. Acquired title: {c.CERT}.", css=css)
