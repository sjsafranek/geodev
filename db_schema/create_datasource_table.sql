
DROP TABLE IF EXISTS datasource CASCADE;


CREATE TABLE datasource (
	id 				VARCHAR NOT NULL UNIQUE DEFAULT md5(random()::text || now()::text)::uuid,
	name 			VARCHAR(64),
	type 			VARCHAR(32) NOT NULL,
	source   		VARCHAR(512) UNIQUE NOT NULL,
	description 	VARCHAR(256),
    srid 			INTEGER NOT NULL DEFAULT 4269,	
	is_updatable 	BOOLEAN DEFAULT false,
    is_deleted 		BOOLEAN DEFAULT false,
    created_at 		TIMESTAMP DEFAULT current_timestamp,
    updated_at 		TIMESTAMP DEFAULT current_timestamp
);

DROP TRIGGER IF EXISTS datasource_update ON layer;
CREATE TRIGGER datasource_update BEFORE UPDATE ON datasource FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE INDEX idx_datasource_name ON datasource(name);

INSERT INTO datasource(name, type, source) VALUES ('openstreetmap', 'TiledMapService', 'https://tile.openstreetmap.org/{z}/{x}/{y}.png');

