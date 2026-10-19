#!/usr/bin/env python3
"""Render the profile's System windows.

  python3 scripts/build.py static              # header, buttons, quests, skills, footer -> assets/
  python3 scripts/build.py live --snake S.svg  # status + daily quest from live data -> dist/

`live` reads GITHUB_TOKEN from the environment (the Actions token is enough).
Standard library only, so the workflow needs no install step.
"""

import argparse
import json
import os
import pathlib
import sys
from dataclasses import asdict

from system import cards, content, hero, skills, stats
from system.daily_quest import render_daily_quest
from system.status import render_status

ROOT = pathlib.Path(__file__).resolve().parent.parent


def write(out_dir, files):
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, svg in files.items():
        (out_dir / name).write_text(svg, encoding="utf-8")
        print(f"  {out_dir.name}/{name}  {len(svg) / 1024:.1f} KB")


def build_static(out_dir):
    files = {
        "header.svg": hero.render_header(),
        "footer.svg": hero.render_footer(),
        "quest-log.svg": cards.render_quest_divider(),
        "skills.svg": skills.render_skills(),
        **cards.render_buttons(),
        **cards.render_quests(),
    }
    write(out_dir, files)


def build_live(out_dir, snake_path):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    s = stats.fetch(content.LOGIN, token)
    snake = pathlib.Path(snake_path).read_text(encoding="utf-8")
    write(out_dir, {
        "status.svg": render_status(s),
        "daily-quest.svg": render_daily_quest(snake, s),
        "stats.json": json.dumps(asdict(s), indent=2) + "\n",
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)
    st = sub.add_parser("static")
    st.add_argument("--out", default=ROOT / "assets", type=pathlib.Path)
    lv = sub.add_parser("live")
    lv.add_argument("--snake", required=True, help="SVG produced by Platane/snk")
    lv.add_argument("--out", default=ROOT / "dist", type=pathlib.Path)
    args = parser.parse_args()

    if args.mode == "static":
        build_static(args.out)
    else:
        build_live(args.out, args.snake)


if __name__ == "__main__":
    main()
