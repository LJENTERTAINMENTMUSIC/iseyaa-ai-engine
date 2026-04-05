-- Phase 5 Migration: Events Marketplace & Governance (OEMG)

-- ─── Events ───────────────────────────────
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    event_date TIMESTAMPTZ NOT NULL,
    lga_id TEXT NOT NULL,
    venue TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Festival', 'Concert', 'Corporate', 'Community', 'Sport')),
    ticket_price DECIMAL(12, 2) DEFAULT 0.0,
    merchant_id UUID REFERENCES merchants(id), -- Organizer
    image_url TEXT,
    status TEXT DEFAULT 'discovered' CHECK (status IN ('discovered', 'pending', 'verified', 'completed', 'cancelled')),
    discovery_source TEXT DEFAULT 'crawler',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Ticketing ───────────────────────────────
CREATE TABLE IF NOT EXISTS tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES events(id),
    user_id UUID NOT NULL,
    booking_id UUID REFERENCES bookings(id),
    qr_code TEXT UNIQUE,
    status TEXT DEFAULT 'valid' CHECK (status IN ('valid', 'used', 'cancelled')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Public can view verified events. Organizers can manage their own.
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public view verified events" ON events FOR SELECT 
    USING (status = 'verified' OR status = 'completed');

CREATE POLICY "Users view own tickets" ON tickets FOR SELECT 
    USING (user_id = auth.uid());
