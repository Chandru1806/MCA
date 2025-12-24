"""
Migration script to change is_active from BOOLEAN to VARCHAR(1)
Run this in PostgreSQL before testing the new endpoints
"""

-- Step 1: Change column type to VARCHAR(1)
ALTER TABLE users 
ALTER COLUMN is_active TYPE VARCHAR(1) USING 
    CASE 
        WHEN is_active = TRUE THEN 'A'
        WHEN is_active = FALSE THEN 'I'
        ELSE 'A'
    END;

-- Step 2: Set default value to 'A'
ALTER TABLE users 
ALTER COLUMN is_active SET DEFAULT 'A';

-- Step 3: Add check constraint
ALTER TABLE users 
ADD CONSTRAINT chk_is_active CHECK (is_active IN ('A', 'I'));
