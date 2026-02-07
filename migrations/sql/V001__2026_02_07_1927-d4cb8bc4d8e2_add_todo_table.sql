BEGIN;

-- Running upgrade da33bbc9a4c2 -> d4cb8bc4d8e2

CREATE TABLE todo (
    id SERIAL NOT NULL, 
    title VARCHAR NOT NULL, 
    description VARCHAR(500), 
    completed BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id)
);


COMMIT;

