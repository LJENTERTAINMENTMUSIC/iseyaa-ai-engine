-- Phase 5 Migration: Governance & Aggregator Layers (OHA)

-- ─── Merchants & Hosts ───────────────────────────────
CREATE TABLE IF NOT EXISTS merchants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name TEXT NOT NULL,
    lga_id TEXT NOT NULL,
    contact_person TEXT,
    contact_phone TEXT,
    contact_email TEXT,
    tax_id TEXT UNIQUE, -- State Tax Identification Number
    status TEXT DEFAULT 'discovered' CHECK (status IN ('discovered', 'pending', 'verified', 'suspended')),
    discovery_source TEXT DEFAULT 'manual', -- e.g., 'crawler', 'manual', 'referral'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Link existing stays to merchants if possible
ALTER TABLE stays ADD COLUMN IF NOT EXISTS merchant_id UUID REFERENCES merchants(id);

-- ─── Governance (Tax & Escrow) ───────────────────────────────
CREATE TABLE IF NOT EXISTS tax_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL REFERENCES bookings(id),
    merchant_id UUID NOT NULL REFERENCES merchants(id),
    levy_amount DECIMAL(12, 2) NOT NULL, -- The state's cut (e.g. 5%)
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'collected', 'remitted')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Governments can see all merchants, merchants can see their own.
ALTER TABLE merchants ENABLE ROW LEVEL SECURITY;
ALTER TABLE tax_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Govt view all merchants" ON merchants FOR SELECT TO authenticated
    USING (EXISTS (SELECT 1 FROM users WHERE users.id = auth.uid() AND users.role = 'govt'));

CREATE POLICY "Merchants view own profile" ON merchants FOR SELECT TO authenticated
    USING (id IN (SELECT merchant_id FROM users WHERE users.id = auth.uid()));
