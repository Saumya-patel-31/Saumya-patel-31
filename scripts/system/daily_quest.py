"""The Daily Quest window: Platane/snk's contribution snake inside a System frame."""

import re

from .theme import HOLO_SOFT, MUTED, PENALTY, TEXT, divider, document, text, window

SNAKE_ROOT = re.compile(r"\s*(?:<\?xml[^>]*>\s*)?<svg\b([^>]*)>(.*)</svg>\s*$", re.S)


def embed_snake(svg, *, x, y, width):
    """Nest snk's SVG at (x, y), scaled to `width`, keeping its own CSS animation intact."""
    match = SNAKE_ROOT.match(svg)
    if not match:
        raise ValueError("snake file is not a single <svg> document")
    attrs, inner = match.groups()
    vb = re.search(r'viewBox="([^"]+)"', attrs)
    if not vb:
        raise ValueError("snake <svg> has no viewBox")
    _, _, vw, vh = (float(v) for v in vb.group(1).split())
    height = width * vh / vw
    return f'<svg x="{x}" y="{y}" width="{width}" height="{height:.1f}" viewBox="{vb.group(1)}">{inner}</svg>', height


def render_daily_quest(snake_svg, s):
    w = 884
    snake, snake_h = embed_snake(snake_svg, x=16, y=108, width=w - 32)
    bottom = 108 + snake_h
    h = round(bottom + 72)

    headline = (
        f'<text x="{w / 2}" y="72" class="mono" font-size="14" fill="{TEXT}" text-anchor="middle">'
        f'<tspan fill="{HOLO_SOFT}">[Daily Quest: Contribution Hunt]</tspan> has arrived.</text>'
    )
    goal = (
        f"GOAL  devour all {s.contributions_1y:,} contributions from the last 12 months"
        f"  ·  current streak {s.current_streak}d"
    )
    parts = [
        headline,
        text(w / 2, 96, goal, size=12, color=MUTED, anchor="middle"),
        snake,
        divider(28, w - 28, bottom + 14, opacity=0.18),
        f'<circle class="blink" cx="{w / 2 - 312}" cy="{bottom + 39}" r="4" fill="{PENALTY}"/>',
        text(w / 2 + 8, bottom + 44,
             "WARNING: Failure to complete the daily quest will result in an appropriate penalty.",
             size=12, color=PENALTY, anchor="middle"),
    ]
    win, css = window(8, 8, w, h, title="DAILY QUEST", uid="dq", body="".join(parts))
    title = (
        f"Daily quest: a snake eats {s.contributions_1y} contributions from the last 12 months "
        f"on the contribution grid. Current streak {s.current_streak} days."
    )
    return document(w + 16, h + 16, win, title=title, css=css)
