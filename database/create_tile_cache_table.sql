
DROP TABLE IF EXISTS tile_cache CASCADE;


CREATE UNLOGGED TABLE tile_cache (
	datasource_id	VARCHAR NOT NULL,
	x 				INTEGER NOT NULL,
	y 				INTEGER NOT NULL,
	z 				INTEGER NOT NULL,
	tile 			BYTEA,
	created_at 		TIMESTAMP DEFAULT NOW(),
	expires_at 		TIMESTAMP DEFAULT NOW() + '1 month',
	CONSTRAINT fk_datasource
    	FOREIGN KEY(datasource_id)
	  		REFERENCES datasource(id)

);

CREATE INDEX idx_tile_cache_xyz ON tile_cache(x, y, z);



CREATE OR REPLACE FUNCTION tile_cache__expire_rows_func() RETURNS VOID AS
$$
BEGIN
	DELETE FROM tile_cache WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION tile_cache__expire_rows_func_trigger() RETURNS TRIGGER AS
$$
BEGIN
	PERFORM tile_cache__expire_rows_func();
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER tile_cache__expire_rows_trigger
	AFTER INSERT ON tile_cache
	FOR EACH ROW 
	EXECUTE PROCEDURE tile_cache__expire_rows_func_trigger();

