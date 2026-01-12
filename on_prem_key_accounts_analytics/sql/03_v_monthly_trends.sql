CREATE OR REPLACE VIEW v_monthly_trends AS
SELECT
  *,
  total_volume_liters
    - LAG(total_volume_liters) OVER (PARTITION BY account ORDER BY sale_month) AS mom_volume_liters,
  (total_volume_liters
    - LAG(total_volume_liters) OVER (PARTITION BY account ORDER BY sale_month))
    / NULLIF(LAG(total_volume_liters) OVER (PARTITION BY account ORDER BY sale_month), 0) AS mom_volume_pct,

  total_sales_dollars
    - LAG(total_sales_dollars) OVER (PARTITION BY account ORDER BY sale_month) AS mom_sales_dollars,
  (total_sales_dollars
    - LAG(total_sales_dollars) OVER (PARTITION BY account ORDER BY sale_month))
    / NULLIF(LAG(total_sales_dollars) OVER (PARTITION BY account ORDER BY sale_month), 0) AS mom_sales_pct,

  total_volume_liters
    - LAG(total_volume_liters, 12) OVER (PARTITION BY account ORDER BY sale_month) AS yoy_volume_liters,
  (total_volume_liters
    - LAG(total_volume_liters, 12) OVER (PARTITION BY account ORDER BY sale_month))
    / NULLIF(LAG(total_volume_liters, 12) OVER (PARTITION BY account ORDER BY sale_month), 0) AS yoy_volume_pct,

  AVG(total_volume_liters) OVER (
    PARTITION BY account
    ORDER BY sale_month
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS roll3_volume_liters
FROM v_monthly_scorecard;
