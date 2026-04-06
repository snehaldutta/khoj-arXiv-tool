import httpx
from .rateLimiter import RateLimiter
from .models import Paper
from typing import Literal
from xml.etree import ElementTree as ET

ATOM_NS = "http://www.w3.org/2005/Atom"


class ArXivClient:
    def __init__(self, rate_limit: RateLimiter):
        self._rate_limit = rate_limit
        self._client = httpx.AsyncClient()
        self._baseUrl = "https://export.arxiv.org/api/query"

    async def fetch(
        self,
        query: str,
        sort_by: Literal["relevance", "lastUpdatedDate", "submittedDate"] = "relevance",
    ) -> list[Paper]:

        params: dict[str, str | int] = {
            "search_query": f"all:{query}",
            "sortBy": sort_by,
            "max_results": 10,
        }

        try:
            await self._rate_limit.acquire()
            response = await self._client.get(self._baseUrl, params=params)
            response.raise_for_status()
            return self._parse(response.text)
        except Exception:
            return []

    def _parse(self, xml_text: str) -> list[Paper]:

        papers = []
        try:
            root = ET.fromstring(xml_text)
            if root.tag != f"{{{ATOM_NS}}}feed":
                return papers
            entries = root.findall(f"{{{ATOM_NS}}}entry")
            if not entries:
                return papers
            for entry in entries:
                title_elem = entry.find(f"{{{ATOM_NS}}}title")
                title = (
                    title_elem.text.strip()
                    if title_elem is not None and title_elem.text
                    else ""
                )
                authors = [
                    name_elem.text.strip()
                    for author in entry.findall(f"{{{ATOM_NS}}}author")
                    if (name_elem := author.find(f"{{{ATOM_NS}}}name")) is not None
                    and name_elem.text
                ]
                summary_elem = entry.find(f"{{{ATOM_NS}}}summary")
                summary = (
                    summary_elem.text.strip()
                    if summary_elem is not None and summary_elem.text
                    else ""
                )
                link_elem = entry.find(f"{{{ATOM_NS}}}id")
                link = (
                    link_elem.text.strip()
                    if link_elem is not None and link_elem.text
                    else ""
                )
                pub_date_elem = entry.find(f"{{{ATOM_NS}}}published")
                pub_date = (
                    pub_date_elem.text.strip()
                    if pub_date_elem is not None and pub_date_elem.text
                    else ""
                )
                papers.append(Paper(title, authors, link, summary, pub_date))
            return papers
        except Exception:
            return []
