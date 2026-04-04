-- 001_create_destinations.sql
-- Table for ISEYAA destinations (matches frontend expectations)

create table if not exists destinations (
    id            text primary key,
    title         text not null,
    location      text not null,
    category      text not null,
    rating        numeric not null,
    image         text not null,
    description   text,
    tags          jsonb default '[]'::jsonb,
    opening_hours text,
    entry_fee     text
);

-- Seed data (same as the in‑memory list)
insert into destinations (id, title, location, category, rating, image, description, tags, opening_hours, entry_fee)
values
('olumo-rock', 'Olumo Rock', 'Abeokuta, Ogun State', 'Heritage', 4.9, '/olumo-rock.png',
 'A sacred granite monolith rising 137m from the tropical forest canopy, revered for over 500 years by the Egba people. Offers breathtaking panoramic views of Abeokuta city below.',
 '["historical","heritage","views","hiking","UNESCO"]',
 '8:00 AM – 6:00 PM daily', '₦500 adults, ₦250 children'),

('ogun-forest-canopy', 'Ogun Forest Canopy Walk', 'Ogun Forest Reserve', 'Nature', 4.8, '/jungle-interior.png',
 'Walk beneath a living cathedral of giant monstera leaves and ancient rainforest giants. God rays of sunlight pierce the canopy in a mystical display of natural light.',
 '["nature","forest","ecotourism","photography","wildlife"]',
 '7:00 AM – 5:00 PM (guided tours only)', '₦1,000 per person (guide included)'),

('ogun-waterfall', 'Ogun Jungle Waterfall', 'Ogun–Osun Forest Reserve', 'Nature', 4.9, '/waterfall.png',
 'A multi‑tiered cascade plunging into emerald pools deep within the rainforest. Mist from the falls keeps the surrounding jungle impossibly lush.',
 '["waterfall","swimming","nature","hiking","photography"]',
 '8:00 AM – 4:00 PM', '₦800 adults'),

('ojude-oba-festival', 'Ojude Oba Festival', 'Ijebu-Ode, Ogun State', 'Festival', 5.0, '/festival.png',
 'Nigeria''s most spectacular cultural celebration — thousands gather in stunning ancestral Yoruba regalia for a horse parade that dates back over 150 years.',
 '["festival","culture","Yoruba","annual","heritage","horses"]',
 'Annual event (Eid al-Adha)', 'Free public event'),

('palm-forest', 'Coastal Palm Forest', 'Ogun Coastal Belt', 'Nature', 4.7, '/palm-canopy.png',
 'Walk beneath towering coconut palms toward an infinite azure sky. A serene, meditative experience deep in Ogun''s coastal palm groves.',
 '["palms","coastal","peaceful","nature","relaxation"]',
 'Open access', 'Free')
on conflict (id) do nothing;
