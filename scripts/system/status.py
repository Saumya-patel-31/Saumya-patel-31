"""The Status Window: level, XP and stats, all computed from live GitHub data."""

from . import content as c
from .theme import (DIM, GLOW, HOLO, HOLO_SOFT, ICE, LINE, MUTED, TEXT, VIOLET, delay, divider,
                    document, text, text_width, window)

LANG_COLORS = [HOLO, VIOLET, HOLO_SOFT, GLOW, "#0ea5e9", "#6366f1", DIM]


def _key(y, label):
    return text(36, y, label, size=11.5, color=MUTED, spacing=1.5)


def _stat_columns(w, s):
    stats = [
        ("STR", s.contributions_1y, "contributions · 1y"),
        ("AGI", s.pull_requests, "pull requests"),
        ("PER", s.repos_contributed, "repos contributed to"),
        ("VIT", s.longest_streak, "best streak · days"),
        ("INT", s.public_repos, "public repos"),
    ]
    col = (w - 72) / len(stats)
    out = []
    for i, (label, value, caption) in enumerate(stats):
        cx = 36 + col * (i + 0.5)
        if i:
            out.append(f'<path d="M{36 + col * i:g} 238V318" stroke="{LINE}"/>')
        out.append(f'<g class="rise" {delay(0.5 + i * 0.12)}>')
        out.append(text(cx + 1.5, 254, label, size=14, color=HOLO, cls="sans", anchor="middle", weight=700, spacing=3))
        out.append(text(cx, 294, f"{value:,}", size=34, color=ICE, cls="sans", anchor="middle", weight=700))
        out.append(text(cx, 314, caption, size=10.5, color=MUTED, anchor="middle"))
        out.append("</g>")
    return "".join(out)


def _affinity(w, s):
    x0, x1, y = 150, w - 40, 358
    total = sum(n for _, n in s.languages) or 1
    bar, legend = [], []
    x, lx = x0, x0
    for i, (name, n) in enumerate(s.languages):
        color = LANG_COLORS[min(i, len(LANG_COLORS) - 1)]
        seg = (x1 - x0) * n / total
        bar.append(f'<rect x="{x:.1f}" y="{y}" width="{max(seg - 2, 1):.1f}" height="10" rx="2" fill="{color}"/>')
        label = f"{name} {n}"
        legend.append(f'<rect x="{lx}" y="{y + 25}" width="8" height="8" rx="1.5" fill="{color}"/>')
        legend.append(text(lx + 14, y + 33, label, size=11, color=TEXT))
        x += seg
        lx += 14 + text_width(label, 11) + 16
    return (
        _key(y + 9, "AFFINITY")
        + f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="10" rx="2" fill="{LINE}"/>'
        + f'<g class="grow">{"".join(bar)}</g>'
        + "".join(legend)
        + text(x1, y + 33, "primary language · public repos", size=10, color=DIM, anchor="end")
    )


def render_status(s):
    w, h = 884, 508
    span = max(s.xp_next - s.xp_floor, 1)
    frac = min(max((s.xp - s.xp_floor) / span, 0), 1)
    bar_x0, bar_x1 = 72, w - 40

    parts = [
        _key(84, "NAME"), text(118, 84, c.NAME, size=24, color=ICE, cls="sans", weight=700),
        _key(114, "JOB"), text(118, 114, c.JOB, size=16, color=TEXT, cls="sans"),
        _key(140, "TITLE"), text(118, 140, c.TITLE, size=16, color=GLOW, cls="sans", weight=600),
        _key(166, "GUILD"), text(118, 166, c.GUILD, size=16, color=TEXT, cls="sans"),
        # Level: a purple bloom behind a crisp numeral.
        text(w - 40, 72, "LEVEL", size=12, color=MUTED, anchor="end", spacing=3),
        text(w - 40, 144, str(s.level), size=72, color=VIOLET, cls="sans", anchor="end", weight=800,
             extra='filter="url(#glow-strong)" opacity=".85"'),
        text(w - 40, 144, str(s.level), size=72, color=ICE, cls="sans", anchor="end", weight=800),
        text(w - 40, 166, f"next · LV.{s.level + 1}", size=11, color=MUTED, anchor="end"),
        # XP bar
        text(bar_x0, 186, "1 XP = 1 lifetime contribution", size=10, color=DIM),
        text(bar_x1, 186, f"{s.xp:,} / {s.xp_next:,} XP", size=11, color=MUTED, anchor="end"),
        text(36, 201, "XP", size=11.5, color=HOLO, weight=700),
        f'<rect x="{bar_x0}" y="192" width="{bar_x1 - bar_x0}" height="10" rx="5" fill="{LINE}"/>',
        f'<rect class="grow" x="{bar_x0}" y="192" width="{(bar_x1 - bar_x0) * frac:.1f}" height="10" rx="5" '
        f'fill="url(#xp)" filter="url(#glow)"/>',
        divider(28, w - 28, 222, opacity=0.18),
        _stat_columns(w, s),
        divider(28, w - 28, 336, opacity=0.18),
        _affinity(w, s),
        divider(28, w - 28, 410, opacity=0.18),
        _key(440, "QUEST"),
        f'<path d="M134 432l4 4-4 4-4-4z" fill="{HOLO}"/>',
        text(150, 440, c.CURRENT_QUEST, size=13, color=TEXT),
        _key(466, "PARTY"),
        f'<path class="blink" d="M134 458l4 4-4 4-4-4z" fill="{VIOLET}"/>',
        text(150, 466, c.PARTY, size=13, color=GLOW),
        text(w - 40, 466, f"synced {s.synced}", size=10, color=DIM, anchor="end"),
    ]
    win, css = window(8, 8, w, h, title="STATUS", uid="st", body="".join(parts))
    summary = (
        f"Status window for {c.NAME}. Level {s.level}. {s.contributions_1y} contributions in the last year, "
        f"{s.pull_requests} pull requests, {s.repos_contributed} repos contributed to, best streak "
        f"{s.longest_streak} days, {s.public_repos} public repos. Current quest: {c.CURRENT_QUEST}. {c.PARTY}."
    )
    return document(w + 16, h + 16, win, title=summary, css=css)

