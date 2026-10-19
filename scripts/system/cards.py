"""Small linkable pieces: contact buttons, the Quest Log divider and quest cards.

Each is its own SVG because a README image can only link to one place.
"""

from . import content as c
from .theme import (HOLO, HOLO_SOFT, ICE, MUTED, TEXT, VIOLET, chip, corners, divider, document,
                    text, text_width, title_bar, window)

LINKEDIN_GLYPH = (
    f'<rect x="1.2" y="1.2" width="21.6" height="21.6" rx="4" fill="none" stroke="{ICE}" stroke-width="1.8"/>'
    + text(12, 17, "in", size=13, color=ICE, cls="sans", anchor="middle", weight=800)
)
GLOBE_GLYPH = (
    f'<g fill="none" stroke="{ICE}" stroke-width="1.6"><circle cx="12" cy="12" r="10"/>'
    f'<ellipse cx="12" cy="12" rx="4.4" ry="10"/><path d="M2 12h20M3.8 7h16.4M3.8 17h16.4"/></g>'
)


def render_button(label, sub, glyph):
    w, h = 238, 52
    body = (
        f'<g transform="translate(6 6)">'
        f'<rect width="{w}" height="{h}" rx="6" fill="url(#panel)"/>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="none" stroke="{HOLO}" stroke-opacity=".55"/>'
        + corners(w, h, length=10, width=1.6, offset=2)
        + f'<g transform="translate(16 14)">{glyph}</g>'
        + text(54, 24, label, size=14, color=ICE, cls="sans", weight=700, spacing=3)
        + text(54, 41, sub, size=11, color=MUTED)
        + f'<path class="blink" d="M{w - 26} 19l7 7-7 7" fill="none" stroke="{HOLO}" stroke-width="2"/>'
        + "</g>"
    )
    return document(w + 12, h + 12, body, title=f"{label.title()}: {sub}")


def render_buttons():
    return {
        "btn-linkedin.svg": render_button(*c.LINKEDIN, LINKEDIN_GLYPH),
        "btn-portfolio.svg": render_button(*c.PORTFOLIO, GLOBE_GLYPH),
    }


def render_quest_divider():
    w, h = 900, 74
    body = title_bar(w, 34, "QUEST LOG") + text(
        w / 2, 62, f"{len(c.QUESTS)} gates open · select one to enter", size=11, color=MUTED, anchor="middle"
    )
    return document(w, h, body, title="Quest log")


def _rank_badge(x, y, rank):
    return (
        f'<path d="M{x} {y - 22}l22 22-22 22-22-22z" fill="{VIOLET}" fill-opacity=".16" stroke="{VIOLET}" '
        f'stroke-width="1.6" filter="url(#glow)"/>'
        + text(x, y + 8, rank, size=22, color=ICE, cls="sans", anchor="middle", weight=800)
        + text(x, y + 38, "RANK", size=9, color=MUTED, anchor="middle", spacing=2)
    )


def render_quest(q):
    w, h = 434, 238
    pad = 28
    max_chars = int((w - 2 * pad) / text_width("x", 12))
    for line in q.lines:
        if len(line) > max_chars:
            raise ValueError(f"{q.slug}: line is {len(line)} chars, max {max_chars}: {line!r}")

    kind_color = VIOLET if q.kind == "MAIN QUEST" else HOLO
    kind_chip, kind_w = chip(pad, 46, q.kind, color=kind_color)
    parts = [kind_chip]
    if q.live:
        lx = pad + kind_w + 16
        parts.append(f'<circle class="blink" cx="{lx:g}" cy="41.5" r="3.5" fill="{HOLO_SOFT}" filter="url(#glow)"/>')
        parts.append(text(lx + 10, 46, q.live, size=10.5, color=HOLO_SOFT, spacing=1.5))
    parts += [
        _rank_badge(w - 48, 52, q.rank),
        text(pad, 92, q.name.upper(), size=26, color=ICE, cls="sans", weight=800, spacing=2),
        text(pad, 114, q.tagline, size=12.5, color=HOLO_SOFT),
        divider(pad, w - pad, 128, opacity=0.18),
    ]
    for i, line in enumerate(q.lines):
        parts.append(text(pad, 150 + i * 18, line, size=12, color=TEXT))
    x = pad
    for tag in q.tags:
        tag_svg, tag_w = chip(x, 210, tag, fill_opacity=0.05, text_color=TEXT, spacing=0.5)
        parts.append(tag_svg)
        x += tag_w + 8

    win, css = window(8, 8, w, h, uid=q.slug, body="".join(parts))
    title = f"{q.kind.title()}: {q.name}, {q.tagline}. " + " ".join(q.lines) + " Stack: " + ", ".join(q.tags) + "."
    return document(w + 16, h + 16, win, title=title, css=css)


def render_quests():
    return {f"quest-{q.slug}.svg": render_quest(q) for q in c.QUESTS}
