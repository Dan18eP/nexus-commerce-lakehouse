-- Modelo Gold: Agregación de valor de mercado y estadísticas por país
SELECT
    country,
    COUNT(*) AS total_players,
    ROUND(AVG(age), 1) AS avg_age,
    ROUND(AVG(market_value_in_eur), 2) AS avg_market_value_eur,
    ROUND(SUM(market_value_in_eur), 2) AS total_market_value_eur
FROM {{ ref('players_clean') }}
GROUP BY country
ORDER BY total_market_value_eur DESC
