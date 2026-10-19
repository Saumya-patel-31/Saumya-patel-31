"""The Status Window: level, XP and stats, all computed from live GitHub data."""

from . import content as c
from .theme import (DIM, GLOW, HOLO, HOLO_SOFT, ICE, LINE, MUTED, TEXT, VIOLET, delay, divider,
                    document, text, text_width, window)

LANG_COLORS = [HOLO, VIOLET, HOLO_SOFT, GLOW, "#0ea5e9", "#6366f1", DIM]
PICK_STEP = 1.6  # seconds the job-path cursor rests on each option


def _key(y, label):
    return text(36, y, label, size=11.5, color=MUTED, spacing=1.5)


def _job_paths(x, y):
    """Job Change prompt: path options with a cursor that cycles between them."""
    size, spacing, h = 12.5, 1.5, 26
    out = [text(x, y, c.JOB_PREFIX, size=16, color=TEXT, cls="sans")]
    bx = x + text_width(c.JOB_PREFIX, 16, mono=False) + 14
    for i, path in enumerate(c.JOB_PATHS):
        label = path.upper()
        bw = text_width(label, size, mono=False, spacing=spacing) + 24
        top = y - 18
        first = " first" if i == 0 else ""
        out += [
            f'<rect x="{bx:g}" y="{top}" width="{bw:g}" height="{h}" rx="4" fill="{HOLO}" fill-opacity=".06" '
            f'stroke="{HOLO}" stroke-opacity=".45"/>',
            f'<g class="pick{first}" style="animation-delay:{i * PICK_STEP:g}s">'
            f'<rect x="{bx:g}" y="{top}" width="{bw:g}" height="{h}" rx="4" fill="{VIOLET}" fill-opacity=".35" '
            f'stroke="{GLOW}" stroke-width="1.5" filter="url(#glow)"/>'
            f'<path d="M{bx - 12:g} {top + 7}l7 6-7 6z" fill="{GLOW}"/></g>',
            text(bx + bw / 2 + spacing / 2, y - 0.5, label, size=size, color=ICE, cls="sans", anchor="middle",
                 weight=700, spacing=spacing),
        ]
        bx += bw + 20
    out.append(text(x, y + 28, "[!]", size=11, color=GLOW, cls="mono blink"))
    out.append(text(x + 28, y + 28, c.JOB_PROMPT, size=11, color=HOLO_SOFT))
    cycle = PICK_STEP * len(c.JOB_PATHS)
    css = (
        f".pick{{opacity:0;animation:pick {cycle:g}s step-end infinite}}.pick.first{{opacity:1}}"
        f"@keyframes pick{{0%{{opacity:1}}{100 / len(c.JOB_PATHS):.3f}%{{opacity:0}}}}"
    )
    return "".join(out), css


def _top_stats(w, y):
    gap, h = 14, 78
    cw = (w - 72 - gap * (len(c.TOP_STATS) - 1)) / len(c.TOP_STATS)
    out = []
    for i, st in enumerate(c.TOP_STATS):
        x = 36 + i * (cw + gap)
        if text_width(st.value, 17, mono=False) > cw - 32:
            raise ValueError(f"top stat value too long for its card: {st.value!r}")
        accent = VIOLET if st.highlight else HOLO
        out.append(f'<g class="rise" {delay(0.3 + i * 0.12)}>')
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{h}" rx="6" fill="{accent}" '
            f'fill-opacity="{0.14 if st.highlight else 0.06}" stroke="{accent}" stroke-opacity=".5"/>'
            f'<rect x="{x:.1f}" y="{y + 12}" width="3" height="{h - 24}" rx="1.5" fill="{accent}" filter="url(#glow)"/>'
        )
        label_color = GLOW if st.highlight else HOLO
        out.append(text(x + 18, y + 24, st.label, size=10.5, color=label_color, spacing=2))
        out.append(text(x + 18, y + 50, st.value, size=17, color=ICE, cls="sans", weight=700))
        out.append(text(x + 18, y + 67, st.sub, size=10.5, color=MUTED))
        if st.highlight:
            out.append(f'<circle class="blink" cx="{x + cw - 18:.1f}" cy="{y + 20}" r="3.5" fill="{GLOW}" '
                       f'filter="url(#glow)"/>')
        out.append("</g>")
    return "".join(out)


def _stat_columns(w, y, s):
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
            out.append(f'<path d="M{36 + col * i:g} {y}V{y + 80}" stroke="{LINE}"/>')
        out.append(f'<g class="rise" {delay(0.7 + i * 0.12)}>')
        out.append(text(cx + 1.5, y + 16, label, size=14, color=HOLO, cls="sans", anchor="middle", weight=700,
                        spacing=3))
        out.append(text(cx, y + 56, f"{value:,}", size=34, color=ICE, cls="sans", anchor="middle", weight=700))
        out.append(text(cx, y + 76, caption, size=10.5, color=MUTED, anchor="middle"))
        out.append("</g>")
    return "".join(out)


def _affinity(w, y, s):
    x0, x1 = 150, w - 40
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
    w, h = 884, 586
    span = max(s.xp_next - s.xp_floor, 1)
    frac = min(max((s.xp - s.xp_floor) / span, 0), 1)
    bar_x0, bar_x1 = 72, w - 40
    job, job_css = _job_paths(118, 180)

    parts = [
        _key(84, "NAME"), text(118, 84, c.NAME, size=24, color=ICE, cls="sans", weight=700),
        _key(114, "TITLE"), text(118, 114, c.TITLE, size=16, color=GLOW, cls="sans", weight=700),
        _key(142, "GUILD"), text(118, 142, c.GUILD, size=16, color=TEXT, cls="sans"),
        _key(180, "JOB"), job,
        # Level: a purple bloom behind a crisp numeral.
        text(w - 40, 72, "LEVEL", size=12, color=MUTED, anchor="end", spacing=3),
        text(w - 40, 144, str(s.level), size=72, color=VIOLET, cls="sans", anchor="end", weight=800,
             extra='filter="url(#glow-strong)" opacity=".85"'),
        text(w - 40, 144, str(s.level), size=72, color=ICE, cls="sans", anchor="end", weight=800),
        text(w - 40, 166, f"next · LV.{s.level + 1}", size=11, color=MUTED, anchor="end"),
        # XP bar
        text(bar_x0, 236, "1 XP = 1 lifetime contribution", size=10, color=DIM),
        text(bar_x1, 236, f"{s.xp:,} / {s.xp_next:,} XP", size=11, color=MUTED, anchor="end"),
        text(36, 251, "XP", size=11.5, color=HOLO, weight=700),
        f'<rect x="{bar_x0}" y="242" width="{bar_x1 - bar_x0}" height="10" rx="5" fill="{LINE}"/>',
        f'<rect class="grow" x="{bar_x0}" y="242" width="{(bar_x1 - bar_x0) * frac:.1f}" height="10" rx="5" '
        f'fill="url(#xp)" filter="url(#glow)"/>',
        _top_stats(w, 274),
        divider(28, w - 28, 370, opacity=0.18),
        _stat_columns(w, 386, s),
        divider(28, w - 28, 484, opacity=0.18),
        _affinity(w, 506, s),
        text(w - 40, h - 18, f"synced {s.synced}", size=10, color=DIM, anchor="end"),
    ]
    win, css = window(8, 8, w, h, title="STATUS", uid="st", body="".join(parts))
    top = " ".join(f"{t.label.title()}: {t.value}." for t in c.TOP_STATS)
    summary = (
        f"Status window for {c.NAME}, {c.TITLE}. Level {s.level}. {top} "
        f"Job: {c.JOB_PREFIX} {' / '.join(c.JOB_PATHS)}. {s.contributions_1y} contributions in the last year, "
        f"{s.pull_requests} pull requests, {s.repos_contributed} repos contributed to, best streak "
        f"{s.longest_streak} days, {s.public_repos} public repos."
    )
    return document(w + 16, h + 16, win, title=summary, css=css + job_css)
