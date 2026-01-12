CREATE OR REPLACE VIEW v_distribution_changes AS
WITH stores_by_month AS (
  SELECT DISTINCT
    county AS account,
    sale_month,
    store_id
  FROM v_sales_clean
),
cur AS (
  SELECT account, sale_month, store_id
  FROM stores_by_month
),
prev AS (
  SELECT account, sale_month + INTERVAL '1 month' AS sale_month, store_id
  FROM stores_by_month
),
joined AS (
  SELECT
    COALESCE(c.account, p.account) AS account,
    COALESCE(c.sale_month, p.sale_month) AS sale_month,
    c.store_id AS cur_store_id,
    p.store_id AS prev_store_id
  FROM cur c
  FULL JOIN prev p
    ON c.account = p.account
   AND c.sale_month = p.sale_month
   AND c.store_id = p.store_id
)
SELECT
  account,
  sale_month,
  COUNT(*) FILTER (WHERE prev_store_id IS NULL AND cur_store_id IS NOT NULL) AS gained_locations,
  COUNT(*) FILTER (WHERE cur_store_id IS NULL AND prev_store_id IS NOT NULL) AS lost_locations,
  (COUNT(*) FILTER (WHERE prev_store_id IS NULL AND cur_store_id IS NOT NULL)
   - COUNT(*) FILTER (WHERE cur_store_id IS NULL AND prev_store_id IS NOT NULL)) AS net_location_change
FROM joined
GROUP BY 1,2;
