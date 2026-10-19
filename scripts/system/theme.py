"""The look every System window shares: palette, fonts, frames and effects.

Each panel is a standalone SVG shown through an <img> tag on GitHub, so
everything here is inline: no scripts, no external fonts, no external files.
"""

import random
from xml.sax.saxutils import escape, quoteattr

# ── palette ──────────────────────────────────────────────────────────────
INK = "#050b17"           # deepest background
PANEL_TOP = "#0b1a33"
PANEL_BOTTOM = "#060f21"
HOLO = "#38bdf8"          # System blue
HOLO_SOFT = "#7dd3fc"
ICE = "#e6f4ff"           # headline text
TEXT = "#c3d8ef"          # body text
MUTED = "#7f9ec2"
DIM = "#45628a"
LINE = "#1c3454"
SHADOW = "#7c3aed"        # Shadow Monarch purple
VIOLET = "#a855f7"
GLOW = "#c4b5fd"
PENALTY = "#fb7185"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

# Rough glyph widths in em, used only where layout depends on text width.
MONO_ADVANCE = 0.6
SANS_ADVANCE = 0.64


def text_width(text, size, *, mono=True, spacing=0.0):
    advance = MONO_ADVANCE if mono else SANS_ADVANCE
    return len(text) * (size * advance + spacing)


BASE_CSS = f"""
.mono{{font-family:{MONO}}}
.sans{{font-family:{SANS}}}
.corner{{animation:corner-pulse 3.2s ease-in-out infinite}}
@keyframes corner-pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
.rise{{animation:rise .7s cubic-bezier(.2,.8,.2,1) both}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.fade{{animation:fade .8s ease-out both}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.blink{{animation:blink 1.1s steps(2,jump-none) infinite}}
@keyframes blink{{50%{{opacity:.15}}}}
.open{{transform-box:fill-box;transform-origin:center;animation:open .75s cubic-bezier(.2,.9,.25,1.1) both}}
@keyframes open{{0%{{opacity:0;transform:scale(.55,.02)}}45%{{opacity:1;transform:scale(1,.02)}}100%{{opacity:1;transform:none}}}}
.grow{{transform-box:fill-box;transform-origin:left center;animation:grow 1.4s cubic-bezier(.2,.8,.2,1) .4s both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:none}}}}
.mote{{animation:mote linear infinite both}}
@keyframes mote{{0%{{opacity:0;transform:translateY(0)}}15%{{opacity:.9}}80%{{opacity:.6}}100%{{opacity:0;transform:translateY(var(--rise))}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

BASE_DEFS = f"""
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{PANEL_TOP}" stop-opacity=".97"/>
  <stop offset="1" stop-color="{PANEL_BOTTOM}" stop-opacity=".98"/>
</linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{HOLO}" stop-opacity="0"/>
  <stop offset=".85" stop-color="{HOLO}" stop-opacity=".04"/>
  <stop offset="1" stop-color="{HOLO_SOFT}" stop-opacity=".12"/>
</linearGradient>
<linearGradient id="xp" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{HOLO}"/>
  <stop offset="1" stop-color="{VIOLET}"/>
</linearGradient>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
  <path d="M24 0H0V24" fill="none" stroke="{LINE}" stroke-width=".6" opacity=".55"/>
</pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="2.4" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glow-strong" x="-50%" y="-80%" width="200%" height="260%">
  <feGaussianBlur stdDeviation="7" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
"""


def attr(value):
    return quoteattr(str(value))


def text(x, y, content, *, size, color=TEXT, cls="mono", anchor="start",
         weight=None, spacing=None, extra=""):
    parts = [f'<text x="{x:g}" y="{y:g}" class="{cls}" font-size="{size}" fill="{color}"']
    if anchor != "start":
        parts.append(f' text-anchor="{anchor}"')
    if weight:
        parts.append(f' font-weight="{weight}"')
    if spacing:
        parts.append(f' letter-spacing="{spacing}"')
    if extra:
        parts.append(" " + extra)
    parts.append(f">{escape(content)}</text>")
    return "".join(parts)


def document(width, height, body, *, title, css="", defs=""):
    """Wrap a panel's body in a standalone, accessible SVG document."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label={attr(title)}>'
        f"<title>{escape(title)}</title>"
        f"<style>{BASE_CSS}{css}</style>"
        f"<defs>{BASE_DEFS}{defs}</defs>"
        f"{body}</svg>\n"
    )


def corners(w, h, *, length=22, color=HOLO, width=2.4, offset=3):
    o, n = offset, length - offset
    d = (
        f"M{-o} {n}V{-o}H{n}"
        f"M{w - n} {-o}H{w + o}V{n}"
        f"M{-o} {h - n}V{h + o}H{n}"
        f"M{w - n} {h + o}H{w + o}V{h - n}"
    )
    return (
        f'<path class="corner" d="{d}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="square" filter="url(#glow)"/>'
    )


def title_bar(w, y, title, *, icon=False):
    """A centred window title flanked by fading rules, like the System's tabs."""
    size, spacing = 15, 6
    tw = text_width(title, size, mono=False, spacing=spacing)
    cx = w / 2
    left_end = cx - tw / 2 - (44 if icon else 18)
    right_start = cx + tw / 2 + 18
    out = [
        f'<path d="M28 {y - 5}H{left_end:g}M{right_start:g} {y - 5}H{w - 28}" stroke="{HOLO}" stroke-opacity=".35"/>',
        f'<path d="M{left_end:g} {y - 9}l4 4-4 4-4-4zM{right_start:g} {y - 9}l4 4-4 4-4-4z" fill="{HOLO}"/>',
        text(cx + spacing / 2, y, title, size=size, color=ICE, cls="sans", anchor="middle",
             weight=700, spacing=spacing, extra='filter="url(#glow)"'),
    ]
    if icon:
        ix = cx - tw / 2 - 22
        out.append(
            f'<rect x="{ix - 10:g}" y="{y - 16}" width="20" height="20" rx="4" fill="none" '
            f'stroke="{HOLO}" stroke-width="1.6"/>'
        )
        out.append(text(ix, y - 1, "!", size=14, color=HOLO, cls="sans blink", anchor="middle", weight=800))
    return "".join(out)


def window(x, y, w, h, *, title=None, icon=False, uid="w", sweep=True, opening=False, body=""):
    """A System window: glass panel, grid, scan sweep, glowing corner brackets."""
    clip = f"clip-{uid}"
    parts = [
        f'<clipPath id="{clip}"><rect width="{w}" height="{h}" rx="8"/></clipPath>',
        f'<rect width="{w}" height="{h}" rx="8" fill="url(#panel)"/>',
        f'<rect width="{w}" height="{h}" rx="8" fill="url(#grid)" opacity=".5"/>',
    ]
    css = ""
    if sweep:
        band = 140
        parts.append(
            f'<g clip-path="url(#{clip})"><rect class="sweep-{uid}" y="{-band}" width="{w}" '
            f'height="{band}" fill="url(#sweep)"/></g>'
        )
        css = (
            f".sweep-{uid}{{animation:sweep-{uid} 7s linear infinite}}"
            f"@keyframes sweep-{uid}{{from{{transform:translateY(0)}}to{{transform:translateY({h + band}px)}}}}"
        )
    parts += [
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8" fill="none" stroke="{HOLO}" stroke-opacity=".5"/>',
        f'<rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="5" fill="none" stroke="{HOLO}" stroke-opacity=".12"/>',
        corners(w, h),
    ]
    if title:
        parts.append(title_bar(w, 36, title, icon=icon))
    parts.append(body)
    inner = "".join(parts)
    if opening:
        inner = f'<g class="open">{inner}</g>'
    return f'<g transform="translate({x} {y})">{inner}</g>', css


def divider(x1, x2, y, *, opacity=0.25):
    return f'<path d="M{x1:g} {y:g}H{x2:g}" stroke="{HOLO}" stroke-opacity="{opacity}"/>'


def motes(width, height, *, count, seed, colors=(VIOLET, GLOW, HOLO), band=None):
    """Rising particles ("mana motes"). Seeded so rebuilds are byte-stable."""
    rng = random.Random(seed)
    top, bottom = band or (0, height)
    out = []
    for _ in range(count):
        x = rng.uniform(8, width - 8)
        y = rng.uniform(bottom - 40, bottom)
        r = rng.choice((0.9, 1.2, 1.6, 2.1))
        dur = rng.uniform(6, 13)
        delay = -rng.uniform(0, dur)
        rise = -(rng.uniform(0.45, 0.95) * (bottom - top))
        out.append(
            f'<circle class="mote" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{rng.choice(colors)}" '
            f'style="--rise:{rise:.0f}px;animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>'
        )
    return "".join(out)


def delay(seconds):
    return f'style="animation-delay:{seconds:g}s"'


def chip(x, y, label, *, color=HOLO, fill_opacity=0.08, size=10.5, spacing=1.5, text_color=None):
    """A small bracketed tag. Returns (svg, width) so callers can lay chips out in a row."""
    w = text_width(label, size, spacing=spacing) + 18
    h = size + 10
    svg = (
        f'<rect x="{x:g}" y="{y - h + 5:g}" width="{w:g}" height="{h:g}" rx="3" fill="{color}" '
        f'fill-opacity="{fill_opacity}" stroke="{color}" stroke-opacity=".55"/>'
        + text(x + w / 2 + spacing / 2, y, label, size=size, color=text_color or color, anchor="middle", spacing=spacing)
    )
    return svg, w
