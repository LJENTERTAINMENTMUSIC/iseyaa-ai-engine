-- Phase 4 & 5 Migration: Commercial Hub (StayHub & MoveHub)

-- ─── StayHub (Accommodation) ───────────────────────────────
CREATE TABLE IF NOT EXISTS stays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    lga_id TEXT NOT NULL, -- Logical link to LGA profiles
    category TEXT NOT NULL CHECK (category IN ('Hotel', 'Short-let', 'Resort', 'Homestay')),
    price_per_night DECIMAL(12, 2) NOT NULL,
    image_url TEXT,
    rating DECIMAL(2, 1) DEFAULT 4.0,
    description TEXT,
    amenities TEXT[] DEFAULT '{}',
    location_name TEXT NOT NULL,
    coordinates JSONB, -- {lat: 0.0, lng: 0.0}
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    item_id UUID NOT NULL, -- Either a stay_id or experience_id
    item_type TEXT NOT NULL CHECK (item_type IN ('stay', 'experience', 'mobility')),
    check_in TIMESTAMPTZ,
    check_out TIMESTAMPTZ,
    total_price DECIMAL(12, 2),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── MoveHub (Mobility) ───────────────────────────────
CREATE TABLE IF NOT EXISTS mobility_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    service_type TEXT NOT NULL CHECK (service_type IN ('shuttle', 'private-hire', 'tour-bus')),
    base_lga TEXT NOT NULL,
    contact_info JSONB,
    rating DECIMAL(2, 1) DEFAULT 4.5,
    verified BOOLEAN DEFAULT TRUE
);

-- RLS: Basic policies for commercial data
ALTER TABLE stays ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Stays are publicly viewable" ON stays FOR SELECT USING (true);
CREATE POLICY "Users view own bookings" ON bookings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users create bookings" ON bookings FOR INSERT WITH CHECK (auth.uid() = user_id);
