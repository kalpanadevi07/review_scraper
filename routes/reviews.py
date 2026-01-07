from fastapi import APIRouter, Query
from scraper.review_scraper import ReviewScraper
from scraper.review_analyzer import ReviewAnalyzer
from services.link_extractor_service import LinkExtractorService

router = APIRouter()

scraper = ReviewScraper()
analyzer = ReviewAnalyzer()
link_service = LinkExtractorService()

@router.get("/reviews")
def get_reviews(company_url: str = Query(...), max_reviews: int = 10):
    """
    Scrape employee reviews, analyze sentiment,
    and extract all company website links.
    """

    scraped_data = scraper.scrape_all_sources(company_url, max_reviews)

    analysis = analyzer.analyze(scraped_data["reviews"])

    links_data = link_service.extract_links(company_url)

    scraped_data["analysis"] = analysis
    scraped_data["company_links"] = links_data

    return {
        "status": "success",
        "data": scraped_data
    }
