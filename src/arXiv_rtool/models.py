from dataclasses import dataclass


@dataclass
class Paper:
    title: str
    authors: list[str]
    url: str
    summary: str | None = None
    published_date: str | None = None
