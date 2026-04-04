import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# LGA Intelligence Profiles (Module 1 — Knowledge Graph)
LGA_PROFILES = {
    "abeokuta-south": {
        "name": "Abeokuta South",
        "region": "Egba",
        "origin_story": "Founded in 1830 by Sodeke after the Egba people escaped the Oyo Empire, using Olumo Rock as a natural fortress. This 'refuge under the rock' gave the city its name.",
        "notable_rulers": ["Alake of Egbaland (Oba Adedotun Aremu Gbadebo III)"],
        "economic_focus": ["Tourism", "Adire Textiles", "Civil Service"],
        "history_snip": "The heart of the Egba Confederacy and a historic node for Nigerian Christianity and education."
    },
    "ijebu-ode": {
        "name": "Ijebu Ode",
        "region": "Ijebu",
        "origin_story": "According to tradition, the town was founded by Obanta, an immigrant from Ile-Ife, who defeated the native rulers to establish the Ijebu Kingdom. It is a major node of trade between the coast and the hinterland.",
        "notable_rulers": ["Awujale of Ijebuland (Oba Sikiru Kayode Adetona)"],
        "economic_focus": ["Trade", "Agriculture", "Logistics"],
        "history_snip": "Home to the world-renowned Ojude Oba Festival, a symbol of religious harmony and cultural extravagance."
    },
    "sagamu": {
        "name": "Sagamu",
        "region": "Remo",
        "origin_story": "A confederation of 13 separate towns established in the 19th century to unite the Remo people against external threats. Its location makes it the 'Gateway' between Lagos and the rest of the country.",
        "notable_rulers": ["Akarigbo of Remoland (Oba Babatunde Adewale Ajayi)"],
        "economic_focus": ["Kolanut Trade", "Industrial Manufacturing", "Cement Production"],
        "history_snip": "The world's headquarters for Kolanut trade and a vital industrial hub for West Africa."
    }
}

# In‑memory fallback data (expanded with PRD v1.1 seed data)
_FALLBACK_DESTINATIONS = [
    {
        "id": "olumo-rock",
        "title": "Olumo Rock",
        "location": "Abeokuta, Ogun South",
        "lga": "abeokuta-south",
        "category": "Heritage",
        "rating": 4.9,
        "image": "/olumo-rock.png",
        "description": "A sacred granite monolith rising 137m from the tropical forest canopy, revered for over 500 years by the Egba people. Offers breathtaking panoramic views of Abeokuta city below.",
        "tags": ["historical", "heritage", "views", "hiking", "UNESCO"],
        "opening_hours": "8:00 AM – 6:00 PM daily",
        "entry_fee": "₦500 adults",
    },
    {
        "id": "ojude-oba-precinct",
        "title": "Awujale Palace (Ojude Oba)",
        "location": "Ijebu-Ode, Ogun State",
        "lga": "ijebu-ode",
        "category": "Heritage",
        "rating": 5.0,
        "image": "/festival.png",
        "description": "The ancestral seat of the Ijebu Kingdom. Every year, thousands gather here for the horse parades and cultural displays of the Ojude Oba festival.",
        "tags": ["palace", "culture", "monarch", "archaeology", "photography"],
        "opening_hours": "Contact Palace Office for tours",
        "entry_fee": "Free public access to exterior",
    },
    {
        "id": "sagamu-kola-market",
        "title": "Akarigbo Kolanut Hub",
        "location": "Sagamu, Remo Region",
        "lga": "sagamu",
        "category": "Experience",
        "rating": 4.6,
        "image": "/market.png",
        "description": "The historical heart of the world's kolanut trade. Witness the ancient grading and trading traditions that have powered the Remo economy for a century.",
        "tags": ["market", "economic", "agriculture", "trade-history"],
        "opening_hours": "7:00 AM – 4:00 PM (Best visiting time)",
        "entry_fee": "Free",
    },
    {
        "id": "ogun-forest-canopy",
        "title": "Ogun Forest Canopy Walk",
        "location": "Ogun Forest Reserve",
        "lga": "remains-unmapped",
        "category": "Nature",
        "rating": 4.8,
        "image": "/jungle-interior.png",
        "description": "Walk beneath a living cathedral of giant monstera leaves and ancient rainforest giants. God rays of sunlight pierce the canopy in a mystical display of natural light.",
        "tags": ["nature", "forest", "ecotourism", "photography", "wildlife"],
        "opening_hours": "7:00 AM – 5:00 PM",
        "entry_fee": "₦1,000",
    },
    {
        "id": "ogun-waterfall",
        "title": "Ogun Jungle Waterfall",
        "location": "Osun Forest Reserve",
        "lga": "remains-unmapped",
        "category": "Nature",
        "rating": 4.9,
        "image": "/waterfall.png",
        "description": "A multi‑tiered cascade plunging into emerald pools deep within the rainforest. Mist from the falls keeps the surrounding jungle impossibly lush.",
        "tags": ["waterfall", "swimming", "nature", "hiking", "photography"],
        "opening_hours": "8:00 AM – 4:00 PM",
        "entry_fee": "₦800",
    }
]

_pool = None

async def get_pool():
    global _pool
    if not DATABASE_URL:
        return None
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    return _pool

async def fetch_lga_profile(lga_id: str):
    return LGA_PROFILES.get(lga_id.lower())

async def fetch_destinations(limit: int = 10, category: str = None):
    if not DATABASE_URL:
        data = _FALLBACK_DESTINATIONS
        if category and category.lower() != "all":
            data = [d for d in data if d["category"].lower() == category.lower()]
        return data[:limit]
    # (Existing DB logic stays here if active)
    return _FALLBACK_DESTINATIONS[:limit] # Simplified for Seed Sprint

async def fetch_destination_by_id(dest_id: str):
    return next((d for d in _FALLBACK_DESTINATIONS if d["id"] == dest_id), None)

async def search_destinations(query: str):
    q = query.lower()
    results = []
    for dest in _FALLBACK_DESTINATIONS:
        score = 0
        if q in dest["title"].lower(): score += 10
        if q in dest["location"].lower(): score += 5
        if score > 0:
            results.append({**dest, "_score": score})
    return sorted(results, key=lambda x: x["_score"], reverse=True)
