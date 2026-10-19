"""Full-bleed canvases: the System Notification header and the ARISE footer."""

from . import content as c
from .theme import (DIM, GLOW, HOLO, HOLO_SOFT, ICE, INK, MUTED, SHADOW, TEXT, VIOLET,
                    delay, divider, document, motes, text, text_width, window)

W = 900


def _backdrop(h, *, sky, fog):
    defs = (
        f'<radialGradient id="sky" cx=".5" cy="0" r=".75"><stop offset="0" stop-color="{HOLO}" stop-opacity="{sky}"/>'
        f'<stop offset="1" stop-color="{HOLO}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="fog" cx=".5" cy="1.05" r=".7"><stop offset="0" stop-color="{SHADOW}" stop-opacity="{fog}"/>'
        f'<stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="canvas"><rect width="{W}" height="{h}" rx="16"/></clipPath>'
    )
    body = (
        f'<rect width="{W}" height="{h}" rx="16" fill="{INK}"/>'
        f'<g clip-path="url(#canvas)">'
        f'<rect width="{W}" height="{h}" fill="url(#grid)" opacity=".3"/>'
        f'<rect width="{W}" height="{h}" fill="url(#sky)"/>'
        f'<rect width="{W}" height="{h}" fill="url(#fog)"/>'
    )
    return defs, body


def render_header():
    h = 384
    defs, body = _backdrop(h, sky=0.16, fog=0.5)
    body += motes(W, h, count=38, seed=7) + "</g>"

    ww, wh = 720, 288
    cx = ww / 2
    line = "You have acquired the qualifications to be a Player."
    lw = text_width(line, 15) + 24

    inner = [
        # The System "types" its message: a clip that widens left to right.
        f'<clipPath id="type"><rect x="{cx - lw / 2:g}" y="62" height="36" width="{lw:g}">'
        f'<animate attributeName="width" values="0;0;{lw:g}" keyTimes="0;.32;1" dur="2.3s" fill="freeze"/>'
        f"</rect></clipPath>",
        text(cx, 88, line, size=15, color=TEXT, anchor="middle", extra='clip-path="url(#type)"'),
        text(cx + 6, 154, c.NAME.upper(), size=50, color=ICE, cls="sans rise", anchor="middle", weight=800,
             spacing=12, extra=f'filter="url(#glow)" {delay(2.2)}'),
        text(cx, 190, c.ROLE, size=16, color=HOLO_SOFT, cls="mono rise", anchor="middle", extra=delay(2.5)),
        text(cx, 216, f"{c.SCHOOL}  ·  {c.CERT}", size=13, color=MUTED, cls="mono rise", anchor="middle",
             extra=delay(2.7)),
        f'<g class="fade" {delay(3.0)}>',
        divider(120, ww - 120, 234, opacity=0.18),
        text(cx + 4, 266, "Will you accept?", size=14, color=TEXT, anchor="end"),
        f'<rect class="yes" x="{cx + 20}" y="247" width="80" height="27" rx="4" fill="{VIOLET}" fill-opacity=".22" '
        f'stroke="{VIOLET}" stroke-width="1.5" filter="url(#glow)"/>',
        text(cx + 61.5, 265.5, "YES", size=13, color=ICE, cls="sans", anchor="middle", weight=700, spacing=3),
        f'<rect x="{cx + 112}" y="247" width="62" height="27" rx="4" fill="none" stroke="{DIM}" stroke-opacity=".7"/>',
        text(cx + 144.5, 265.5, "NO", size=13, color=DIM, cls="sans", anchor="middle", weight=700, spacing=3),
        "</g>",
    ]
    win, win_css = window((W - ww) // 2, 50, ww, wh, title="NOTIFICATION", icon=True, uid="n",
                          opening=True, body="".join(inner))
    css = win_css + (
        ".yes{animation:yes 2.4s ease-in-out 3.4s infinite}"
        f"@keyframes yes{{50%{{fill-opacity:.45;stroke:{GLOW}}}}}"
    )
    return document(W, h, body + win, title=f"System notification: {c.NAME}, {c.ROLE}. {c.SCHOOL}.",
                    css=css, defs=defs)


def render_footer():
    h = 236
    defs, body = _backdrop(h, sky=0.05, fog=0.7)
    defs += (
        f'<linearGradient id="arise" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GLOW}"/>'
        f'<stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{SHADOW}"/></linearGradient>'
    )
    body += motes(W, h, count=46, seed=11, colors=(VIOLET, GLOW, SHADOW)) + "</g>"
    body += text(W / 2 + 11, 132, "ARISE.", size=88, color="url(#arise)", cls="sans arise", anchor="middle",
                 weight=900, spacing=22, extra='filter="url(#glow-strong)"')
    body += text(W / 2, 184, "[SYSTEM] Quest log closed. See you at the next gate.", size=13, color=MUTED,
                 anchor="middle")
    css = ".arise{animation:arise 4s ease-in-out infinite}@keyframes arise{50%{opacity:.78}}"
    return document(W, h, body, title="ARISE. Thanks for visiting.", css=css, defs=defs)
