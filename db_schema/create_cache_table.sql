
DROP TABLE IF EXISTS cache CASCADE;


CREATE UNLOGGED TABLE cache (
	id 			SERIAL PRIMARY KEY,
	key 		TEXT UNIQUE NOT NULL,
	value 		JSONB,
	created_at 	TIMESTAMP DEFAULT NOW(),
	expires_at 	TIMESTAMP DEFAULT NOW() + '60 minutes'
);

CREATE INDEX idx_cache_key ON cache(key);



CREATE OR REPLACE FUNCTION cache__expire_rows_func() RETURNS VOID AS
$$
BEGIN
	DELETE FROM cache WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION cache__expire_rows_func_trigger() RETURNS TRIGGER AS
$$
BEGIN
	PERFORM cache__expire_rows_func();
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER cache__expire_rows_trigger
	AFTER INSERT ON cache
	FOR EACH ROW 
	EXECUTE PROCEDURE cache__expire_rows_func_trigger();


