import re
from typing import Dict, List

class ReviewAnalyzer:

    POSITIVE_WORDS = [
        "good", "great", "excellent", "supportive", "flexible",
        "growth", "learning", "balance", "benefits", "positive"
    ]

    NEGATIVE_WORDS = [
        "stress", "pressure", "toxic", "workload", "long hours",
        "poor", "bad", "low salary", "management", "negative"
    ]

    def extract_numeric_rating(self, rating: str) -> float:
        try:
            return float(re.findall(r"\d+\.?\d*", rating)[0])
        except:
            return 0.0

    def sentiment_score(self, pros: str, cons: str) -> float:
        pros = pros.lower()
        cons = cons.lower()

        positive_count = sum(word in pros for word in self.POSITIVE_WORDS)
        negative_count = sum(word in cons for word in self.NEGATIVE_WORDS)

        if positive_count + negative_count == 0:
            return 3.0  # neutral sentiment

        score = 3 + (positive_count - negative_count)
        return max(1.0, min(5.0, score))

    def analyze(self, reviews: Dict[str, List[Dict]]) -> Dict:
        ratings = []
        sentiment_scores = []

        for source_reviews in reviews.values():
            for r in source_reviews:
                rating = self.extract_numeric_rating(r.get("rating", ""))
                if rating > 0:
                    ratings.append(rating)

                sentiment = self.sentiment_score(
                    r.get("pros", ""),
                    r.get("cons", "")
                )
                sentiment_scores.append(sentiment)

        avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0
        avg_sentiment = round(sum(sentiment_scores) / len(sentiment_scores), 2) if sentiment_scores else 3

        overall_score = round((0.7 * avg_rating) + (0.3 * avg_sentiment), 2)

        return {
            "average_rating": avg_rating,
            "average_sentiment": avg_sentiment,
            "overall_score": overall_score,
            "rating_scale": "out of 5"
        }
