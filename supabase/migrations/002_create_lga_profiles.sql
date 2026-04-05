-- 002_create_lga_profiles.sql
-- Table for ISEYAA LGA (Local Government Area) Intelligence Profiles

create table if not exists lga_profiles (
    id              text primary key,
    name            text not null,
    region          text not null,
    origin_story    text,
    notable_rulers  jsonb default '[]'::jsonb,
    economic_focus  jsonb default '[]'::jsonb,
    history_snip    text
);

-- Seed data for primary LGAs
insert into lga_profiles (id, name, region, origin_story, notable_rulers, economic_focus, history_snip)
values
('abeokuta-south', 'Abeokuta South', 'Egba', 
 'Founded in 1830 by Sodeke after the Egba people escaped the Oyo Empire, using Olumo Rock as a natural fortress. This "refuge under the rock" gave the city its name.',
 '["Alake of Egbaland (Oba Adedotun Aremu Gbadebo III)"]',
 '["Tourism", "Adire Textiles", "Civil Service"]',
 'The heart of the Egba Confederacy and a historic node for Nigerian Christianity and education.'),

('ijebu-ode', 'Ijebu Ode', 'Ijebu', 
 'According to tradition, the town was founded by Obanta, an immigrant from Ile-Ife, who defeated the native rulers to establish the Ijebu Kingdom. It is a major node of trade between the coast and the hinterland.',
 '["Awujale of Ijebuland (Oba Sikiru Kayode Adetona)"]',
 '["Trade", "Agriculture", "Logistics"]',
 'Home to the world-renowned Ojude Oba Festival, a symbol of religious harmony and cultural extravagance.'),

('sagamu', 'Sagamu', 'Remo', 
 'A confederation of 13 separate towns established in the 19th century to unite the Remo people against external threats. Its location makes it the "Gateway" between Lagos and the rest of the country.',
 '["Akarigbo of Remoland (Oba Babatunde Adewale Ajayi)"]',
 '["Kolanut Trade", "Industrial Manufacturing", "Cement Production"]',
 'The world''s headquarters for Kolanut trade and a vital industrial hub for West Africa.')
on conflict (id) do update set
    name = excluded.name,
    region = excluded.region,
    origin_story = excluded.origin_story,
    notable_rulers = excluded.notable_rulers,
    economic_focus = excluded.economic_focus,
    history_snip = excluded.history_snip;
