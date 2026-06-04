-- Run this once on the production database to add the Jobber OAuth refresh token column
ALTER TABLE business ADD COLUMN IF NOT EXISTS jobber_refresh_token TEXT;
