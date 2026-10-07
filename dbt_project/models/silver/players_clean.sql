-- Modelo Silver: Lee datos limpios o semi-estructurados y estandariza
SELECT
    player_id,
    name,
    age,
    current_club_name,
    country,
    market_value_in_eur,
    processed_at
FROM read_parquet('s3://datalake/silver/football/players_clean.parquet')
WHERE age IS NOT NULL AND market_value_in_eur > 0
