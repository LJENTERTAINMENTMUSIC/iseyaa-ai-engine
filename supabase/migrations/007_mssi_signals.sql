-- Phase 5 Migration: Media Signals & Social Intelligence (MSSI)

-- ─── Media Signals ───────────────────────────────
CREATE TABLE IF NOT EXISTS media_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type TEXT NOT NULL CHECK (source_type IN ('tiktok', 'x', 'linkedin', 'blog', 'google', 'radio', 'tv', 'newspaper')),
    content_summary TEXT NOT NULL,
    sentiment_score DECIMAL(3, 2), -- -1.0 (Critical) to 1.0 (Positive)
    lga_id TEXT, -- Optional regional mapping
    metadata JSONB DEFAULT '{}', -- {original_link: '...', influencer: '...'}
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Discovered Trends ───────────────────────────────
CREATE TABLE IF NOT EXISTS discovered_trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Tourism', 'Governance', 'Economic', 'Security')),
    velocity_score DECIMAL(5, 2) DEFAULT 0.0, -- Measure of growth rate
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'archived', 'flagged')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Governments only for MSSI data
ALTER TABLE media_signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE discovered_trends ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Govt view all signals" ON media_signals FOR SELECT TO authenticated
    USING (EXISTS (SELECT 1 FROM users WHERE users.id = auth.uid() AND users.role = 'govt'));

CREATE POLICY "Govt view all trends" ON discovered_trends FOR SELECT TO authenticated
    USING (EXISTS (SELECT 1 FROM users WHERE users.id = auth.uid() AND users.role = 'govt'));
