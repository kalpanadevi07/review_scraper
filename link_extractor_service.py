##link extractor worked only for qscriptsoftware

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os

class LinkExtractorService:

    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_links(self, company_url: str) -> dict:
        parsed_domain = urlparse(company_url).netloc
        internal_links = set()
        external_links = set()

        try:
            response = requests.get(
                company_url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            soup = BeautifulSoup(response.content, "html.parser")

            for tag in soup.find_all("a", href=True):
                href = tag["href"].strip()
                full_url = urljoin(company_url, href)

                parsed = urlparse(full_url)
                if not parsed.scheme.startswith("http"):
                    continue

                if parsed.netloc == parsed_domain:
                    internal_links.add(full_url)
                else:
                    external_links.add(full_url)

        except Exception as e:
            print(f"Link extraction error: {e}")

        data = {
            "company_website": company_url,
            "internal_links": sorted(list(internal_links)),
            "external_links": sorted(list(external_links)),
            "total_internal_links": len(internal_links),
            "total_external_links": len(external_links)
        }

        self._store_links(data)
        return data

    def _store_links(self, data: dict):
        file_path = os.path.join(self.output_dir, "company_links.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
