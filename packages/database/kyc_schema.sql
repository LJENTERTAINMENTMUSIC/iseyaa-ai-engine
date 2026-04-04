-- ISEYAA Trust & Identity Schema
-- Aligned with Module 7 (Wallet & Wealth) and Module 8 (Govt Dashboard)

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id UUID PRIMARY KEY, -- Linked to Supabase Auth
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'traveler' CHECK (role IN ('traveler', 'host', 'govt')),
    kyc_status TEXT DEFAULT 'unverified' CHECK (kyc_status IN ('unverified', 'pending', 'verified', 'rejected')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS kyc_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    document_type TEXT CHECK (document_type IN ('nin', 'voters_card', 'passport')),
    document_number TEXT NOT NULL,
    file_url TEXT NOT NULL, -- Path to Supabase Storage bucket
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ,
    reviewer_notes TEXT
);

-- Access Control: Allow government officials only if role is 'govt' AND kyc_status is 'verified'
CREATE OR REPLACE VIEW verified_officials AS
SELECT * FROM user_profiles
WHERE role = 'govt' AND kyc_status = 'verified';

-- Trigger to update 'updated_at' column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_modtime
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
