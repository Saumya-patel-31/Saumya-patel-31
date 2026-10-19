"""Live numbers for the Status Window, read from GitHub's GraphQL API."""

import json
import math
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

API = "https://api.github.com/graphql"

PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    pullRequests { totalCount }
    repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY], includeUserRepositories: true) {
      totalCount
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { primaryLanguage { name } }
    }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""

WINDOW_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


@dataclass
class Stats:
    contributions_1y: int
    contributions_all: int
    active_days_1y: int
    current_streak: int
    longest_streak: int
    pull_requests: int
    repos_contributed: int
    public_repos: int
    languages: list[tuple[str, int]]
    level: int
    xp: int
    xp_floor: int
    xp_next: int
    synced: str


def level_for(xp):
    """Level n starts at 2·n² XP: early levels come quickly, later ones slow down."""
    level = math.isqrt(xp // 2)
    return level, 2 * level * level, 2 * (level + 1) ** 2


def _gql(token, query, **variables):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def _days(calendar):
    return {
        d["date"]: d["contributionCount"]
        for week in calendar["weeks"]
        for d in week["contributionDays"]
    }


def _iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def _streaks(days):
    """(current, longest) runs of days with at least one contribution.

    Today may still be empty without breaking the current streak.
    """
    ordered = sorted(days)
    longest = run = 0
    last_active = None
    for key in ordered:
        if days[key] == 0:
            continue
        day = date.fromisoformat(key)
        run = run + 1 if last_active and day - last_active == timedelta(days=1) else 1
        longest = max(longest, run)
        last_active = day

    current = 0
    tail = list(reversed(ordered))
    if tail and days[tail[0]] == 0:
        tail = tail[1:]
    for key in tail:
        if days[key] == 0:
            break
        current += 1
    return current, longest


def fetch(login, token):
    user = _gql(token, PROFILE_QUERY, login=login)
    calendar = user["contributionsCollection"]["contributionCalendar"]
    last_year = _days(calendar)

    # The API caps each query at one year, so walk back to the account's creation in windows.
    all_days = dict(last_year)
    start = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    first_day = datetime.fromisoformat(min(last_year)).replace(tzinfo=timezone.utc)
    while start < first_day:
        end = min(start + timedelta(days=365), first_day)
        window = _gql(token, WINDOW_QUERY, login=login, **{"from": _iso(start), "to": _iso(end)})
        for key, count in _days(window["contributionsCollection"]["contributionCalendar"]).items():
            all_days.setdefault(key, count)
        start = end

    current, longest = _streaks(all_days)
    langs = Counter(
        node["primaryLanguage"]["name"]
        for node in user["repositories"]["nodes"]
        if node["primaryLanguage"]
    )
    total = sum(all_days.values())
    level, floor, nxt = level_for(total)
    return Stats(
        contributions_1y=calendar["totalContributions"],
        contributions_all=total,
        active_days_1y=sum(1 for n in last_year.values() if n > 0),
        current_streak=current,
        longest_streak=longest,
        pull_requests=user["pullRequests"]["totalCount"],
        repos_contributed=user["repositoriesContributedTo"]["totalCount"],
        public_repos=user["repositories"]["totalCount"],
        languages=sorted(langs.items(), key=lambda kv: (-kv[1], kv[0])),
        level=level,
        xp=total,
        xp_floor=floor,
        xp_next=nxt,
        synced=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
