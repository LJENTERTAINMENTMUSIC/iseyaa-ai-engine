"""
MSSI Sentiment Analysis Service — ISEYAA State Operating System
Handles natural language sentiment scoring for all media signals.
"""

import re
from typing import Dict, Any

class SentimentService:
    def __init__(self):
        self.positive_terms = ["great", "beautiful", "verified", "safe", "love", "luxury", "festival", "cultural"]
        self.negative_terms = ["bad", "unsafe", "unverified", "expensive", "slow", "dirty", "poor", "critical"]

    async def analyze_sentiment(self, text: str) -> float:
        """
        Returns a score from -1.0 to 1.0. 
        In Phase 5, this uses the internal LLM provider for deep analysis.
        For the prototype, it uses keyword-weighted scoring.
        """
        text = text.lower()
        pos_count = sum(1 for term in self.positive_terms if term in text)
        neg_count = sum(1 for term in self.negative_terms if term in text)
        
        if pos_count == 0 and neg_count == 0: return 0.0
        
        score = (pos_count - neg_count) / (pos_count + neg_count)
        return round(max(-1.0, min(1.0, score)), 2)

    async def categorize_signal(self, text: str) -> str:
        # Detect if it's Tourism, Economic, or Security related
        if any(w in text.lower() for w in ["hotel", "visit", "tourism", "park", "resort"]):
             return "Tourism"
        if any(w in text.lower() for w in ["business", "investment", "industry", "money"]):
             return "Economic"
        return "Governance"

sentiment_engine = SentimentService()
