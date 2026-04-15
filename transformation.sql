CREATE TABLE raw_hsr_data (
    id SERIAL PRIMARY KEY,
    uid BIGINT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);

select * from raw_hsr_data

SELECT 
  elem->>'character_name' AS CHAR_NAME
  elem->>'' AS HP
  elem->>'' AS ATK
  elem->>'' AS DEF
  elem->>'' AS SPD
  elem->>'' AS CRIT_DMG
  elem->>'' AS CRIT_RATE
  elem->>'' AS CHAR_ID
  
from raw_hsr_data,
jsonb_array_elements(payload->'stats') AS elem;
