import re
import pandas as pd

INDUSTRY_KEYWORDS = {
    "Technology": ["digital", "ai", "semiconductor", "software", "it services", "electronics"],
    "Agriculture": ["agriculture", "farmer", "pulses", "agri-stack", "kisan", "crop"],
    "Infrastructure": ["infrastructure", "railways", "highways", "logistics", "ports", "urban"],
    "Energy": ["green hydrogen", "solar", "nuclear", "ev battery", "renewable", "energy"],
    "Manufacturing": ["msme", "make in india", "pli scheme", "textiles", "manufacturing"],
    "Healthcare": ["biopharma", "healthcare", "medical", "ayush", "pharmaceutical"]
}

def extract_industry_mentions(documents):
    data = []
    for doc in documents:
        # Extract year from filename (e.g., budget_2024.pdf)
        year_match = re.search(r"\d{4}", doc["source"])
        year = year_match.group(0) if year_match else "Unknown"
        
        text_lower = doc["text"].lower()
        
        for category, keywords in INDUSTRY_KEYWORDS.items():
            count = sum(text_lower.count(kw) for kw in keywords)
            data.append({
                "Year": year,
                "Sector": category,
                "Mentions": count,
                "Source": doc["source"]
            })
            
    return pd.DataFrame(data)