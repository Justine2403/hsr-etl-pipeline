CREATE DATABASE hsr_db;

CREATE TABLE raw_hsr_data (
    id SERIAL PRIMARY KEY,
    uid BIGINT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);

SELECT test[0] FROM (
select payload ->> 'stats' AS test
from raw_hsr_data)


CREATE TABLE character_stats AS
SELECT
    (stat->>'character_id')::int AS character_id,
    (stat->>'HP')::numeric AS hp,
    (stat->>'ATK')::numeric AS atk,
    (stat->>'DEF')::numeric AS def,
    (stat->>'SPD')::numeric AS spd,
    (stat->>'CRIT Rate')::numeric AS crit_rate,
    (stat->>'CRIT DMG')::numeric AS crit_dmg
FROM raw_hsr_data,
jsonb_array_elements(payload->'stats') AS stat;

select * from character_stats