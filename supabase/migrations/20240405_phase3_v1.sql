-- Phase 3 Migration: KYC Intelligence Layer
-- Implements persistence for user identity verification

CREATE TABLE IF NOT EXISTS kyc_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL, -- Link to auth.users if using Supabase Auth
    document_type TEXT NOT NULL,
    document_number TEXT NOT NULL,
    file_url TEXT NOT NULL,
    tracking_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('processing', 'verified', 'rejected', 'pending')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast lookup on status checks
CREATE INDEX IF NOT EXISTS idx_kyc_user_latest ON kyc_submissions (user_id, created_at DESC);

-- RLS: Only users can see their own KYC submissions, and govt-admins can see all.
ALTER TABLE kyc_submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own KYC" ON kyc_submissions
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Govt admins can view all KYC" ON kyc_submissions
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid() AND users.role = 'govt'
        )
    );
