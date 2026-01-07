from fastapi import FastAPI
from routes import reviews

app = FastAPI(
    title="Employee Review Scraper",
    description="Scrape employee reviews from AmbitionBox, Glassdoor, and Indeed",
    version="1.0.0"
)

# Include routes
app.include_router(reviews.router, prefix="/api")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Employee Review Scraper API! Use /api/reviews?company_url=<url>"}
