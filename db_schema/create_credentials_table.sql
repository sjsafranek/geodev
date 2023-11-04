
DROP TABLE IF EXISTS credentials CASCADE;

-- @table config
-- @description stores database config info
CREATE TABLE IF NOT EXISTS credentials (
    name            VARCHAR(64) PRIMARY KEY,
    type            VARCHAR(32),
    data           	JSONB,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- @trigger config_update
-- @description update config record
DROP TRIGGER IF EXISTS credentials_update ON credentials;
CREATE TRIGGER credentials_update
    BEFORE UPDATE ON credentials
        FOR EACH ROW
            EXECUTE PROCEDURE update_modified_column();