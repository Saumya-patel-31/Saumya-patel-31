"""Everything the panels say. Edit here, then run `python3 scripts/build.py static`."""

from dataclasses import dataclass, field

LOGIN = "Saumya-patel-31"
NAME = "Saumya Patel"
ROLE = "Software Engineer · AI/ML · Cloud"
SCHOOL = "CS @ UMBC · Class of Dec 2027"
CERT = "AWS Certified ×3"

# Status Window
JOB = "Software Engineer"
TITLE = "One Who Runs LLMs Locally"
GUILD = "UMBC · ex-HeadsUp (SWE Intern)"
CURRENT_QUEST = "Building Prism, a privacy-first local LLM hub"
PARTY = "Open to Summer 2027 SWE / AI internships"

LINKEDIN = ("LINKEDIN", "/in/saumya31")
PORTFOLIO = ("PORTFOLIO", "saumya.world")


@dataclass
class Quest:
    slug: str
    name: str
    rank: str
    tagline: str
    lines: list[str]
    tags: list[str]
    kind: str = "QUEST"
    live: str | None = None


QUESTS = [
    Quest(
        slug="prism",
        name="Prism",
        rank="S",
        kind="MAIN QUEST",
        live="LIVE DEMO",
        tagline="privacy-first local LLM hub",
        lines=[
            "Chat with local models over your own docs:",
            "hybrid RAG (vectors + BM25, fused with RRF),",
            "built-in retrieval evals, zero cloud calls.",
        ],
        tags=["TypeScript", "Ollama", "SQLite", "Terraform"],
    ),
    Quest(
        slug="campusly",
        name="Campusly",
        rank="A",
        live="LIVE",
        tagline="a campus social network",
        lines=[
            "Verified .edu accounts only. Posts, likes,",
            "comments, DMs and follows on Postgres, with",
            "realtime updates over WebSockets.",
        ],
        tags=["React", "Supabase", "PostgreSQL"],
    ),
    Quest(
        slug="meshwork",
        name="meshwork",
        rank="A",
        tagline="everything you follow, one daily email",
        lines=[
            "Watches jobs, GitHub, news, arXiv, Reddit and",
            "any page you pick, dedupes and ranks what's",
            "new, then mails one digest. Every link is real.",
        ],
        tags=["JavaScript", "Python", "Docker"],
    ),
    Quest(
        slug="optionslab",
        name="Optionslab",
        rank="A",
        tagline="options pricing engine",
        lines=[
            "Black-Scholes, binomial and Monte Carlo",
            "pricers that cross-check each other, plus",
            "analytical Greeks and a live IV surface.",
        ],
        tags=["Python", "Streamlit"],
    ),
]


@dataclass
class Skill:
    label: str
    glyph: str  # key in icons.GLYPHS, or "aws" for the hand-drawn stand-in


@dataclass
class SkillGroup:
    name: str
    caption: str
    skills: list[Skill] = field(default_factory=list)


SKILLS = [
    SkillGroup("ACTIVE SKILLS", "languages", [
        Skill("Python", "python"), Skill("TypeScript", "typescript"),
        Skill("JavaScript", "javascript"), Skill("Java", "openjdk"),
        Skill("C", "c"), Skill("C++", "cplusplus"),
    ]),
    SkillGroup("PASSIVE SKILLS", "cloud · data · infra", [
        Skill("AWS", "aws"), Skill("Terraform", "terraform"), Skill("Docker", "docker"),
        Skill("Supabase", "supabase"), Skill("Postgres", "postgresql"),
        Skill("Firebase", "firebase"), Skill("SQLite", "sqlite"), Skill("Linux", "linux"),
    ]),
    SkillGroup("EQUIPMENT", "frameworks · tools", [
        Skill("React", "react"), Skill("Next.js", "nextdotjs"), Skill("Node.js", "nodedotjs"),
        Skill("Tailwind", "tailwindcss"), Skill("Ollama", "ollama"), Skill("Streamlit", "streamlit"),
        Skill("Git", "git"), Skill("Neovim", "neovim"), Skill("Android", "androidstudio"),
    ]),
]
